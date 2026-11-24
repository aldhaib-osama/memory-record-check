"""Validate metadata completeness and expiry in fictional agent-memory records."""
import argparse
from datetime import datetime,timezone
import json


def timestamp(value):
    if not isinstance(value,str):raise ValueError('Timestamp must be text')
    result=datetime.fromisoformat(value.replace('Z','+00:00'))
    if result.tzinfo is None:raise ValueError('Timestamp needs timezone')
    return result.astimezone(timezone.utc)


def check(records,at):
    now=timestamp(at)
    if not isinstance(records,list):raise ValueError('Expected record list')
    ids=set();issues=[]
    required={'id','source_ref','source_kind','scope','created_at','expires_at'}
    for record in records:
        if not isinstance(record,dict):raise ValueError('Record must be object')
        if set(record)!=required:raise ValueError('Record has missing or extra fields')
        if any(not isinstance(record[k],str) or not record[k].strip() for k in required):
            raise ValueError('Metadata values must be nonempty strings')
        ident=record['id']
        if ident in ids:raise ValueError('Duplicate record id')
        ids.add(ident)
        if record['source_kind'] not in {'user_statement','external_claim','derived_summary'}:
            raise ValueError('Unknown source kind')
        if record['scope'] not in {'preference','reference','task_context'}:raise ValueError('Unknown scope')
        created=timestamp(record['created_at']);expires=timestamp(record['expires_at'])
        reasons=[]
        if expires<=created:reasons.append('invalid_time_order')
        if created>now:reasons.append('future_record')
        if expires<=now:reasons.append('expired')
        if record['source_kind']!='user_statement' and record['scope']=='preference':
            reasons.append('source_scope_mismatch')
        if reasons:issues.append({'id':ident,'reasons':reasons})
    return {'records':len(records),'issues':issues,
            'meaning':'Metadata checks only. Source kind is asserted input, not authenticated authority.'}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input');parser.add_argument('--at',required=True)
    args=parser.parse_args(argv)
    try:
        with open(args.input,encoding='utf-8') as f:result=check(json.load(f),args.at)
        print(json.dumps(result,indent=2));return 1 if result['issues'] else 0
    except (OSError,ValueError,TypeError) as e:parser.exit(2,f'Input error: {e}\n')
if __name__=='__main__':raise SystemExit(main())
