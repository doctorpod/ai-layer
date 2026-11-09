#!/usr/bin/env python3
"""
Turn an exported Rails/Docker log into clean, interleaved request traces,
ready to draw sequence diagrams from.

Usage:
  python3 trace-logs.py list    <log> [--date YYYY-MM-DD] [--entry frontend]
  python3 trace-logs.py trace   <log> --from TIME [--to TIME] [options]
  python3 trace-logs.py summary <log>

Subcommands:
  list     One line per user-facing request (the entry service's "Started"
           lines), with the downstream calls it triggered. Use it to find
           the window you want to trace.
  trace    The cleaned, interleaved trace for a time window. With --from
           only, traces the single entry request that starts at or after
           --from, up to its "Completed" line.
  summary  Endpoint counts per service, models touched, and error lines:
           raw material for a system map.

TIME is an ISO prefix compared as text, e.g. 2026-10-26T14:01:43 or
"2026-10-26 14:01:43". UTC, as the export stores it.

Trace options:
  --sql            keep SQL text after model loads (default: dropped)
  --params         keep "Parameters:" lines
  --noise          keep Unpermitted-parameters warnings and partial renders
  --raw-ids        don't shorten OCDS ids to {ocid}

Input: the CSV that Docker Desktop exports (timestamp,object,message).
Plain-text logs are not supported yet; see read_entries().

Caveat: downstream calls are matched to the entry request by timestamp,
not by request id. Fine for a single local user, unreliable under load.
"""

import argparse
import csv
import re
import sys
from collections import Counter
from dataclasses import dataclass

ANSI_RE = re.compile(r'\x1b?\[[0-9;]*m')
OCID_RE = re.compile(r'ocds-[A-Za-z0-9-]+')
STARTED_RE = re.compile(r'^Started (\w+) "([^"]+)" for (\S+)')
PROCESSING_RE = re.compile(r'^Processing by (\S+) as (\S+)')
COMPLETED_RE = re.compile(r'^Completed (\d{3}) (.+?) in (\d+)ms')
REDIRECT_RE = re.compile(r'^Redirected to https?://[^/]+(\S*)')
MODEL_RE = re.compile(r'^(CACHE )?([\w:]+) (Load|Create|Update|Destroy|Count|Exists\?|Delete All|Pluck|Insert|Upsert)\s*\(([\d.]+ms)\)')
TRANSACTION_RE = re.compile(r'^TRANSACTION \([\d.]+ms\)\s+(BEGIN|COMMIT|ROLLBACK)')
CALLSITE_RE = re.compile(r"^↳ (\S+?):(\d+):in [`']([^']+)'")  # Ruby 3.4 'x', older `x'
RENDERED_PAGE_RE = re.compile(r'^Rendered (\S+) within layouts/')
ERROR_RE = re.compile(r'(Error|Exception|rescue_from|FATAL)')

# Lines that never help a diagram.
DROP_RE = re.compile(
    r'^(Rendering |Rendered layouts/|Rendered shared/|Cannot render console|'
    r'DEPRECATION WARNING|More info and automated migrator|Information for|'
    r'ActiveRecord::SchemaMigration|\(Reading database|[│╷╵]|\d+ │|'
    r'Puma|\* |Use Ctrl-C|=> )'
)
NOISE_RE = re.compile(r'^(Unpermitted parameter|Rendered )')


@dataclass
class Entry:
    ts: str
    service: str
    msg: str


def read_entries(path):
    """Yield Entry rows from a log export.

    Only Docker Desktop's CSV export (timestamp,object,message) is handled.
    Plain-text `docker compose logs` output ("service  | message") is the
    obvious next format: detect it here and parse it into the same Entry
    shape, and nothing downstream needs to change.
    """
    with open(path, encoding='utf-8-sig', newline='') as f:
        header = f.readline()
        if not header.lower().startswith('timestamp,object,message'):
            sys.exit(f'{path}: not a Docker Desktop CSV export (expected a '
                     f'"timestamp,object,message" header). Plain-text logs '
                     f'are not supported yet.')
        for row in csv.reader(f):
            if len(row) < 3:
                continue
            ts, obj, msg = row[0], row[1], ','.join(row[2:])
            yield Entry(ts, obj.rsplit('/', 1)[-1], ANSI_RE.sub('', msg).strip())


def tag(service):
    s = service.lower()
    if s.endswith('_db') or s.endswith('-db'):
        return 'DB'
    if 'front' in s:
        return 'FE'
    if 'back' in s:
        return 'BE'
    return service[:6].upper()


def norm_ts(value):
    return value.replace(' ', 'T') if value else value


def short_path(path, raw_ids, limit=110):
    if not raw_ids:
        path = OCID_RE.sub('{ocid}', path)
    return path if len(path) <= limit else path[:limit] + '…'


def clean(msg, opts):
    """Return a compact line for a trace, or None to drop it."""
    if not msg or DROP_RE.match(msg):
        return None
    if NOISE_RE.match(msg) and not RENDERED_PAGE_RE.match(msg):
        return msg if opts.noise else None
    if msg.startswith('Parameters:'):
        return short_path(msg, opts.raw_ids, 160) if opts.params else None

    if m := STARTED_RE.match(msg):
        return f'→ {m.group(1)} {short_path(m.group(2), opts.raw_ids)}'
    if m := PROCESSING_RE.match(msg):
        return f'  {m.group(1)} ({m.group(2)})'
    if m := COMPLETED_RE.match(msg):
        return f'← {m.group(1)} {m.group(2)} in {m.group(3)}ms'
    if m := REDIRECT_RE.match(msg):
        return f'  redirect {short_path(m.group(1), opts.raw_ids)}'
    if m := MODEL_RE.match(msg):
        if m.group(1):  # cached query, no real work
            return None
        line = f'    {m.group(2)} {m.group(3)} ({m.group(4)})'
        if opts.sql:
            line += '  ' + msg[m.end():].strip()[:160]
        return line
    if m := TRANSACTION_RE.match(msg):
        return f'    {m.group(1)}'
    if m := CALLSITE_RE.match(msg):
        return f'      ↳ {m.group(3)}  ({m.group(1)}:{m.group(2)})'
    if m := RENDERED_PAGE_RE.match(msg):
        return f'  render {m.group(1)}'
    if ERROR_RE.search(msg):
        return '  ! ' + short_path(msg, opts.raw_ids, 200)
    if msg.startswith(('SELECT', 'INSERT', 'UPDATE', 'DELETE', 'WITH', 'FROM')):
        return None  # continuation of a multi-line SQL statement
    return None


def entry_services(entries, wanted):
    if wanted:
        return {wanted}
    names = {e.service for e in entries}
    fronts = {n for n in names if tag(n) == 'FE'}
    return fronts or names


def entry_requests(entries, entry_svcs):
    """Pair each entry-service Started line with its Completed line.

    Returns (start_index, end_index) pairs into entries. Pairing is
    sequential per service, which holds for a single local user.
    """
    open_req, pairs = {}, []
    for i, e in enumerate(entries):
        if e.service not in entry_svcs:
            continue
        if STARTED_RE.match(e.msg):
            if e.service in open_req:  # never completed; close it here
                pairs.append((open_req[e.service], i - 1))
            open_req[e.service] = i
        elif COMPLETED_RE.match(e.msg) and e.service in open_req:
            pairs.append((open_req.pop(e.service), i))
    pairs.extend((s, len(entries) - 1) for s in open_req.values())
    return sorted(pairs)


def cmd_list(entries, args):
    svcs = entry_services(entries, args.entry)
    for start, end in entry_requests(entries, svcs):
        e = entries[start]
        if args.date and not e.ts.startswith(args.date):
            continue
        m = STARTED_RE.match(e.msg)
        status = action = ''
        downstream = []
        for x in entries[start + 1:end + 1]:
            if x.service in svcs:
                if p := PROCESSING_RE.match(x.msg):
                    action = p.group(1)
                elif c := COMPLETED_RE.match(x.msg):
                    status = f'{c.group(1)} {c.group(3)}ms'
            elif d := STARTED_RE.match(x.msg):
                downstream.append(f'{d.group(1)} {short_path(d.group(2).split("?")[0], args.raw_ids, 60)}')
        print(f'{e.ts[:23]}  {m.group(1):6} {short_path(m.group(2).split("?")[0], args.raw_ids, 70):70}  {status:12} {action}')
        for d in downstream:
            print(f'{"":25}  └ {d}')


def cmd_trace(entries, args):
    start = norm_ts(args.start)
    end = norm_ts(args.end)
    if not end:
        svcs = entry_services(entries, args.entry)
        match = next(((s, t) for s, t in entry_requests(entries, svcs)
                      if entries[s].ts >= start), None)
        if not match:
            sys.exit(f'No entry request starts at or after {start}.')
        start, end = entries[match[0]].ts, entries[match[1]].ts
    else:
        end = end + '￿'  # make a prefix like 14:02 include 14:02:59.999

    previous = None
    for e in entries:
        if not (start <= e.ts <= end) or tag(e.service) == 'DB':
            continue
        line = clean(e.msg, args)
        if line is None:
            continue
        if line.startswith('      ↳') and previous == line:
            continue
        if line.startswith('→') and tag(e.service) == 'FE':
            print()
        print(f'{e.ts[11:23]} {tag(e.service)} {line}')
        previous = line


def cmd_summary(entries, args):
    endpoints, models, errors = Counter(), Counter(), []
    for e in entries:
        if m := STARTED_RE.match(e.msg):
            path = OCID_RE.sub('{ocid}', m.group(2).split('?')[0])
            path = re.sub(r'/\d+(?=/|$)', '/{id}', path)
            endpoints[(tag(e.service), m.group(1), path)] += 1
        elif m := MODEL_RE.match(e.msg):
            if not m.group(1):
                models[(tag(e.service), m.group(2), m.group(3))] += 1
        elif (COMPLETED_RE.match(e.msg) and not e.msg.startswith(('Completed 2', 'Completed 3'))) \
                or e.msg.startswith(('rescue_from', '[backend_unavailable]', '[invalid_request]')) \
                or re.match(r'^[\w:]+(Error|Exception) \(', e.msg):
            errors.append(f'{e.ts[:19]} {tag(e.service)} {short_path(e.msg, False, 160)}')

    print(f'Span: {entries[0].ts[:19]} to {entries[-1].ts[:19]}, {len(entries)} lines\n')
    print('Endpoints (requests received):')
    for (svc, verb, path), n in sorted(endpoints.items()):
        print(f'  {n:4}  {svc} {verb:6} {path}')
    print('\nModels touched:')
    for (svc, model, op), n in sorted(models.items()):
        print(f'  {n:4}  {svc} {model} {op}')
    print(f'\nNon-2xx/3xx and error lines ({len(errors)}):')
    for line in errors:
        print('  ' + line)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('command', choices=['list', 'trace', 'summary'])
    parser.add_argument('log')
    parser.add_argument('--from', dest='start')
    parser.add_argument('--to', dest='end')
    parser.add_argument('--date')
    parser.add_argument('--entry', help='service that receives user requests (default: the frontend)')
    parser.add_argument('--sql', action='store_true')
    parser.add_argument('--params', action='store_true')
    parser.add_argument('--noise', action='store_true')
    parser.add_argument('--raw-ids', action='store_true')
    args = parser.parse_args()

    entries = sorted(read_entries(args.log), key=lambda e: e.ts)
    if not entries:
        sys.exit(f'{args.log}: no log lines found.')

    if args.command == 'list':
        cmd_list(entries, args)
    elif args.command == 'trace':
        if not args.start:
            sys.exit('trace needs --from (see "list" to find a start time).')
        cmd_trace(entries, args)
    else:
        cmd_summary(entries, args)


if __name__ == '__main__':
    main()
