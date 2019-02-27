import datetime

import pytz
from django.utils.translation import ugettext
from schedule.periods import Period
from django.utils import timezone
from django.template.defaultfilters import date as date_filter
from django.conf import settings


class Hour(Period):
    def __init__(self, events, date=None, parent_persisted_occurrences=None,
                 occurrence_pool=None, tzinfo=pytz.utc):
        self.tzinfo = self._get_tzinfo(tzinfo)
        if date is None:
            date = timezone.now()
        start, end = self._get_hour_range(date)
        super(Hour, self).__init__(events, start, end,
                                  parent_persisted_occurrences, occurrence_pool, tzinfo=tzinfo)

    def _get_hour_range(self, date):

        # localize the date before we typecast to naive dates
        if self.tzinfo is not None and timezone.is_aware(date):
            date = date.astimezone(self.tzinfo)

        naive_start = datetime.datetime.combine(date, date.time())
        naive_end = datetime.datetime.combine((date + datetime.timedelta(hours=1)).date(), (date + datetime.timedelta(hours=1)).time())
        if self.tzinfo is not None:
            local_start = self.tzinfo.localize(naive_start)
            local_end = self.tzinfo.localize(naive_end)
            start = local_start.astimezone(pytz.utc)
            end = local_end.astimezone(pytz.utc)
        else:
            start = naive_start
            end = naive_end

        return start, end

    def __str__(self):
        date_format = 'l, %s' % settings.DATE_FORMAT
        return ugettext('Hour: %(start)s-%(end)s') % {
            'start': date_filter(self.start, date_format),
            'end': date_filter(self.end, date_format),
        }

    def next_hour(self):
        return Hour(self.events, self.end, tzinfo=self.tzinfo)
    next = __next__ = next_hour


class HalfHour(Period):
    def __init__(self, events, date=None, parent_persisted_occurrences=None,
                 occurrence_pool=None, tzinfo=pytz.utc):
        self.tzinfo = self._get_tzinfo(tzinfo)
        if date is None:
            date = timezone.now()
        start, end = self._get_half_hour_range(date)
        super(HalfHour, self).__init__(events, start, end,
                                  parent_persisted_occurrences, occurrence_pool, tzinfo=tzinfo)

    def _get_half_hour_range(self, date):

        # localize the date before we typecast to naive dates
        if self.tzinfo is not None and timezone.is_aware(date):
            date = date.astimezone(self.tzinfo)

        naive_start = datetime.datetime.combine(date, date.time())
        naive_end = datetime.datetime.combine((date + datetime.timedelta(minutes=30)).date(), (date + datetime.timedelta(minutes=30)).time())
        if self.tzinfo is not None:
            local_start = self.tzinfo.localize(naive_start)
            local_end = self.tzinfo.localize(naive_end)
            start = local_start.astimezone(pytz.utc)
            end = local_end.astimezone(pytz.utc)
        else:
            start = naive_start
            end = naive_end

        return start, end

    def __str__(self):
        date_format = 'l, %s' % settings.DATE_FORMAT
        return ugettext('HalfHour: %(start)s-%(end)s') % {
            'start': date_filter(self.start, date_format),
            'end': date_filter(self.end, date_format),
        }

    def next_half_hour(self):
        return HalfHour(self.events, self.end, tzinfo=self.tzinfo)
    next = __next__ = next_half_hour
