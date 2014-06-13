import sys
import os
import json
from datetime import datetime, timedelta
from Cheetah.Template import Template

def get_template(template):
    f = open(template, 'r')
    t = f.read()
    f.close()
    return t

def render_template(template, input):
    template = get_template(template)
    return Template(template, searchList=[input]).__str__()

def write_to_file(filename, output):
    f = open(filename, 'w')
    f.write(output)
    f.close()

def load_json(filename):
    f = open(filename, 'r')
    input = json.load(f)
    f.close()
    return input

def parse_date(date_to_parse):
    return datetime.strptime(date_to_parse, "%d %B %Y")

def pretty_date(orig_date):
    return parse_date(orig_date).strftime("%A %d %B")

def is_this_week(date_to_test, this_sunday):
    sunday_p = parse_date(this_sunday)
    next_sunday_p = sunday_p + timedelta(days=7)
    date_to_test_p = parse_date(date_to_test)
    return date_to_test_p >= sunday_p and date_to_test_p < next_sunday_p

def is_next_week(date_to_test, this_sunday):
    first_sunday = parse_date(this_sunday) + timedelta(days=7)
    second_sunday = first_sunday + timedelta(days=7)
    date_to_test_p = parse_date(date_to_test)
    return date_to_test_p >= first_sunday and date_to_test_p < second_sunday

def is_before_this_week(date_to_test, this_sunday):
    date_to_test_p = parse_date(date_to_test)
    this_sunday_p = parse_date(this_sunday)
    return date_to_test_p <= this_sunday_p

def filter_lessons(lessons, bulletin_date):
    sunday_school = {}
    sunday_school['this_week'] = [lesson for lesson in lessons if is_this_week(lesson['date'], bulletin_date)][0]
    sunday_school['next_week'] = [lesson for lesson in lessons if is_next_week(lesson['date'], bulletin_date)][0]
    return sunday_school, priesthood_rs

def filter_calendar(events, bulletin_date):
    calendar = {}
    calendar['this_week'] = [event for event in events if is_this_week(event['date'], bulletin_date)]
    calendar['next_week'] = [event for event in events if is_next_week(event['date'], bulletin_date)]
    return calendar

def filter_primary(all_weeks, bulletin_date):
    primary = {}
    primary['this_week'] = [week for week in all_weeks if is_this_week(week['date'], bulletin_date)][0]
    primary['next_week'] = [week for week in all_weeks if is_next_week(week['date'], bulletin_date)][0]
    return primary

def filter_orgs(all_orgs, bulletin_date):
    return [org for org in all_orgs if is_before_this_week(org['start_date'], bulletin_date)]

def generate(input_json, template_tex, output_tex):
    print 'Starting bulletin creation'
    print 'Loading JSON configuration %s' % input_json
    input = load_json(input_json)
    calendar = load_json(input['calendar_json'])
    organizations = load_json(input['org_json'])
    lessons = load_json(input['lessons_json'])
    primary = load_json(input['primary_json'])

    input['sunday_school'], input['priesthood_rs'] = filter_lessons(lessons, input['bulletin_date'])
    input['calendar'] = filter_calendar(calendar['events'], input['bulletin_date'])
    input['primary'] = filter_primary(primary['weeks'], input['bulletin_date'])
    input['orgs'] = filter_orgs(organizations['orgs'], input['bulletin_date'])

    print 'Writing output to %s' % output_tex
    write_to_file(output_tex, render_template(template_tex, input))
    print 'Done'

def main(argv):
    if len(argv) < 2:
        print 'Usage: generate.py input_file'
        exit(1)
    input_json = argv[1]
    generate(input_json, 'template.tex', 'bulletin.tex')

if __name__=='__main__':
    main(sys.argv)

