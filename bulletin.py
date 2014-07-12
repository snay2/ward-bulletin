from datetime import datetime, timedelta
import json

class Bulletin:
    def __init__(self, json_file):
        self.input  = self.load_json(json_file)
        self.date   = self.parse_date(self.input['bulletin_date'])

        calendar    = self.load_json(self.input['calendar_json'])
        orgs        = self.load_json(self.input['org_json'])
        lessons     = self.load_json(self.input['lessons_json'])
        primary     = self.load_json(self.input['primary_json'])

        self.input['calendar']      = self.filter_calendar(calendar['events'])
        self.input['orgs']          = self.filter_orgs(orgs['orgs'])
        self.input['sunday_school'] = self.filter_lessons(lessons['lessons'], 'sunday_school')
        self.input['priesthood_rs'] = self.filter_lessons(lessons['lessons'], 'priesthood_rs')
        self.input['primary']       = self.filter_primary(primary['weeks'])

    def load_json(self, filename):
        f = open(filename, 'r')
        input = json.load(f)
        f.close()
        return input

    def get_parameters(self):
        return self.input

    def parse_date(self, date_to_parse):
        return datetime.strptime(date_to_parse, "%d %B %Y")

    def pretty_date(self, item):
        item['date'] = self.parse_date(item['date']).strftime("%A %d %B")
        return item

    def is_this_week(self, item):
        date_to_test = self.parse_date(item['date'])
        return date_to_test >= self.date and date_to_test < (self.date + timedelta(days=7))

    def is_next_week(self, item):
        date_to_test = self.parse_date(item['date'])
        return date_to_test >= (self.date + timedelta(days=7)) and date_to_test < (self.date + timedelta(days=14))

    def is_before_this_week(self, item):
        date_to_test = self.parse_date(item['date'])
        return date_to_test <= self.date

    def filter_calendar(self, events):
        calendar = {}
        calendar['this_week'] = filter(self.is_this_week, events)
        calendar['next_week'] = filter(self.is_next_week, events)
        map(self.pretty_date, calendar['this_week'])
        map(self.pretty_date, calendar['next_week'])
        return calendar

    def filter_orgs(self, orgs):
        return sorted(filter(self.is_before_this_week, orgs), key=lambda org: self.parse_date(org['date']), reverse=True)

    def filter_lessons(self, lessons, type):
        filtered = {}
        filtered['this_week'] = filter(self.is_this_week, lessons)[0][type]
        filtered['next_week'] = filter(self.is_next_week, lessons)[0][type]
        return filtered

    def filter_primary(self, assignments):
        primary = {}
        primary['this_week'] = filter(self.is_this_week, assignments)[0]
        primary['next_week'] = filter(self.is_next_week, assignments)[0]
        return primary

