# -*- coding: utf-8 -*-
"""Deterministic fictional backup data for application 02 (and E2 in the performance test)."""
import random
from datetime import date, datetime, timedelta

from entity import SYSTEMS

WIN_FROM = date(2026, 8, 2)
WIN_TO = date(2026, 9, 30)
DAYS = (WIN_TO - WIN_FROM).days + 1  # 60
PERIOD_END = datetime(2026, 9, 30, 23, 59)

# RPO/RTO targets in hours (asset register for backup)
TARGETS = {
    'SYS-01': (24, 4), 'SYS-02': (24, 4), 'SYS-03': (24, 8), 'SYS-04': (24, 4), 'SYS-05': (24, 24),
    'SYS-06': (24, 8), 'SYS-07': (24, 4), 'SYS-08': (168, 8), 'SYS-09': (168, 24), 'SYS-10': (168, 24),
    'SYS-11': (72, 24),
}
SYS = {s[0]: dict(id=s[0], name=s[1], host=s[3], crit=s[6], cls=s[7]) for s in SYSTEMS}

# Entity backup policy (training assumption values)
POLICY = {
    'retention': {'حرج': 35, 'عالٍ': 30, 'متوسط': 14},
    'monthly_critical': 12,
    'isolated_required': {'حرج'},
    'ticket_required': {'حرج', 'عالٍ'},
    'test_interval_days': {'حرج': 183, 'عالٍ': 365},
}

DAILY, WEEKLY = 'يومي', 'أسبوعي (الجمعة)'
ISO_YES = 'نعم — أرشيف الحصين، تخزين غير قابل للتعديل (Immutable)، يُحدَّث أسبوعياً'

# job id, system, scope, schedule, start (h, m), type, dr copy, isolated, retention days, monthly copies,
# encryption, base duration min, base size GB
JOBS = [
    ('J-01', 'SYS-01', 'قاعدة بيانات البوابة', DAILY, (1, 0), 'تزايدي يومي + كامل أسبوعي', 'نعم', ISO_YES, 35, 12, 'نعم', 42, 180),
    ('J-02', 'SYS-01', 'خوادم تطبيق البوابة (صورة النظام)', WEEKLY, (3, 0), 'كامل', 'نعم', ISO_YES, 35, 0, 'نعم', 95, 410),
    ('J-03', 'SYS-03', 'قاعدة بيانات ERP', DAILY, (23, 0), 'تزايدي يومي + كامل أسبوعي', 'نعم', ISO_YES, 35, 12, 'نعم', 75, 520),
    ('J-04', 'SYS-03', 'خوادم تطبيق ERP (صورة النظام)', WEEKLY, (4, 0), 'كامل', 'نعم', ISO_YES, 35, 0, 'نعم', 110, 380),
    ('J-05', 'SYS-04', 'قاعدة بيانات الموارد البشرية', DAILY, (22, 0), 'تزايدي يومي + كامل أسبوعي', 'نعم', ISO_YES, 35, 12, 'نعم', 38, 140),
    ('J-06', 'SYS-05', 'مستودع الوثائق وقاعدة بياناته', DAILY, (21, 0), 'تزايدي يومي + كامل أسبوعي', 'نعم', 'لا', 14, 0, 'نعم', 130, 2300),
    ('J-07', 'SYS-06', 'صناديق البريد السحابي (نسخ من السحابة إلى منصة الجهة)', DAILY, (2, 0), 'تزايدي', 'نعم', 'لا', 30, 0, 'نعم', 160, 950),
    ('J-08', 'SYS-07', 'حالة النظام لوحدتي تحكم النطاق DC01 وDC02', DAILY, (0, 30), 'كامل', 'نعم', 'لا', 35, 12, 'نعم', 25, 60),
    ('J-09', 'SYS-08', 'إعدادات بوابة VPN', WEEKLY, (5, 0), 'تصدير إعدادات', 'نعم', 'لا', 30, 0, 'نعم', 3, 0.2),
    ('J-10', 'SYS-09', 'إعدادات منصة SIEM وقواعد الكشف', WEEKLY, (5, 30), 'تصدير إعدادات', 'نعم', 'لا', 30, 0, 'نعم', 12, 4),
    ('J-11', 'SYS-10', 'فهرس النسخ وإعدادات منصة النسخ', DAILY, (6, 0), 'كامل', 'نعم', ISO_YES, 30, 0, 'نعم', 9, 6),
    ('J-12', 'SYS-11', 'البوابة الداخلية للموظفين', DAILY, (20, 0), 'تزايدي يومي + كامل أسبوعي', 'نعم', 'لا', 14, 0, 'نعم', 18, 45),
]
JOB = {j[0]: j for j in JOBS}

OK, PART, FAIL = 'ناجح', 'ناجح جزئياً', 'فاشل'
IMAGE_JOBS = {'J-02', 'J-04'}   # server images; data RPO is measured on the database job of the same system
RPO_TOL_H = 2                   # training assumption: tolerance on the gap between backup start times
# (job, date) -> (status, message, ticket, rerun?)
EVENTS = {
    ('J-03', date(2026, 8, 9)): (FAIL, 'انتهت مهلة الاتصال بقاعدة البيانات', 'INC-2026-0815', None),
    ('J-03', date(2026, 8, 10)): (FAIL, 'انتهت مهلة الاتصال بقاعدة البيانات', '', None),
    ('J-03', date(2026, 8, 11)): (FAIL, 'انتهت مهلة الاتصال بقاعدة البيانات', '', None),
    ('J-03', date(2026, 8, 12)): (FAIL, 'انتهت مهلة الاتصال بقاعدة البيانات', '', None),
    ('J-03', date(2026, 8, 27)): (FAIL, 'امتلأت مساحة التخزين المؤقت على خادم النسخ', '', None),
    ('J-03', date(2026, 9, 5)): (PART, 'تم تخطي ملفات سجل المعاملات (قيد الاستخدام)', '', None),
    ('J-03', date(2026, 9, 18)): (FAIL, 'فشل التحقق من بيانات اعتماد حساب الخدمة', '', None),
    ('J-03', date(2026, 9, 19)): (FAIL, 'فشل التحقق من بيانات اعتماد حساب الخدمة', '', None),
    ('J-03', date(2026, 9, 24)): (FAIL, 'انتهت مهلة الاتصال بقاعدة البيانات', '', None),
    ('J-01', date(2026, 8, 30)): (PART, 'تم تخطي 3 ملفات مقفلة', 'INC-2026-0871', (2, 5)),
    ('J-06', date(2026, 8, 21)): (FAIL, 'انقطاع الاتصال بوحدة التخزين', 'INC-2026-0842', (21, 45)),
    ('J-07', date(2026, 9, 7)): (PART, 'تجاوز صندوقان مهلة النسخ', 'INC-2026-0880', (5, 10)),
    ('J-09', date(2026, 9, 11)): (FAIL, 'تعذر الاتصال بواجهة إدارة البوابة', 'INC-2026-0889', (6, 30)),
    ('J-12', date(2026, 9, 2)): (FAIL, 'انتهت مهلة الاتصال بالخادم', '', None),
}

TICKETS = [
    ('INC-2026-0815', '2026-08-10 08:20', 'فشل مهمة نسخ قاعدة بيانات ERP (J-03)', 'J-03', 'مغلقة', '2026-08-10 15:05', 'انقطاع مؤقت في الشبكة؛ لا يلزم إجراء'),
    ('INC-2026-0842', '2026-08-21 21:35', 'فشل مهمة نسخ مستودع الوثائق (J-06)', 'J-06', 'مغلقة', '2026-08-22 00:30', 'أعيد ربط وحدة التخزين وأعيد تشغيل المهمة بنجاح'),
    ('INC-2026-0855', '2026-08-26 10:00', 'طلب استعادة ملف محذوف لمستخدم في نظام الوثائق', '—', 'مغلقة', '2026-08-26 13:15', 'تمت الاستعادة من نسخة 2026-08-24'),
    ('INC-2026-0871', '2026-08-30 01:55', 'نجاح جزئي لمهمة نسخ قاعدة بيانات البوابة (J-01)', 'J-01', 'مغلقة', '2026-08-30 03:00', 'أعيد التشغيل يدوياً بنجاح'),
    ('INC-2026-0880', '2026-09-07 04:55', 'نجاح جزئي لمهمة نسخ البريد السحابي (J-07)', 'J-07', 'مغلقة', '2026-09-07 08:30', 'أعيد نسخ الصندوقين يدوياً بنجاح'),
    ('INC-2026-0889', '2026-09-11 05:25', 'فشل نسخ إعدادات بوابة VPN (J-09)', 'J-09', 'مغلقة', '2026-09-11 07:00', 'أعيد التشغيل يدوياً بنجاح'),
]

RESTORE_TESTS = [
    dict(id='RT-2025-10', d=date(2025, 10, 29), sys='SYS-09', scope='استعادة إعدادات SIEM وقواعد الكشف إلى خادم اختبار', rto=24, actual=95, integrity='مطابقة عدد قواعد الكشف (412 قاعدة)', result='ناجح', sign='م. ماجد الزهراني؛ هشام البلوي', action=''),
    dict(id='RT-2025-11', d=date(2025, 11, 20), sys='SYS-05', scope='استعادة المستودع وقاعدة بياناته إلى بيئة الاختبار', rto=24, actual=540, integrity='فتح عينة 50 وثيقة ومطابقة عدد السجلات', result='ناجح', sign='سارة الرشيدي؛ هشام البلوي', action=''),
    dict(id='RT-2025-12', d=date(2025, 12, 2), sys='SYS-01', scope='استعادة قاعدة بيانات البوابة إلى بيئة الاختبار', rto=4, actual=215, integrity='مطابقة عدد السجلات وتجربة 5 معاملات', result='ناجح', sign='م. تركي السالم؛ هشام البلوي', action=''),
    dict(id='RT-2026-01', d=date(2026, 2, 10), sys='SYS-06', scope='استعادة 5 صناديق بريد إلى صندوق اختبار', rto=8, actual=140, integrity='مطابقة عدد الرسائل', result='ناجح', sign='م. سلطان الغامدي؛ هشام البلوي', action=''),
    dict(id='RT-2026-02', d=date(2026, 3, 18), sys='SYS-08', scope='استعادة إعدادات بوابة VPN إلى جهاز مختبر', rto=8, actual=65, integrity='مقارنة ملف الإعدادات (Hash)', result='ناجح', sign='م. عمر الحازمي؛ هشام البلوي', action=''),
    dict(id='RT-2026-03', d=date(2026, 4, 22), sys='SYS-10', scope='استعادة فهرس النسخ إلى خادم في موقع التعافي', rto=24, actual=180, integrity='مطابقة عدد نقاط الاستعادة في الفهرس', result='ناجح', sign='هشام البلوي', action=''),
    dict(id='RT-2026-04', d=date(2026, 7, 14), sys='SYS-11', scope='استعادة البوابة الداخلية إلى خادم اختبار', rto=24, actual=160, integrity='فتح الصفحات الرئيسية ومطابقة عدد الصفحات', result='ناجح', sign='سارة الرشيدي؛ هشام البلوي', action=''),
    dict(id='RT-2026-05', d=date(2026, 8, 11), sys='SYS-04', scope='استعادة كاملة لقاعدة بيانات الموارد البشرية وخادم التطبيق إلى بيئة معزولة', rto=4, actual=190, integrity='مطابقة عدد السجلات (480 ملفاً وظيفياً)، ومقارنة المجموع الاختباري، وتحقق مستخدم من الموارد البشرية', result='ناجح', sign='منيرة الدوسري؛ هشام البلوي', action=''),
    dict(id='RT-2026-06', d=date(2026, 9, 8), sys='SYS-03', scope='استعادة كاملة لقاعدة بيانات ERP وخوادم التطبيق في موقع التعافي', rto=8, actual=685, integrity='مطابقة أرصدة الحسابات وعدد القيود', result='مكتمل — تجاوز زمن الاستعادة المستهدف', sign='خالد الشمري؛ هشام البلوي', action=''),
]


def _fridays():
    d = WIN_FROM
    out = []
    while d <= WIN_TO:
        if d.weekday() == 4:
            out.append(d)
        d += timedelta(days=1)
    return out


def history():
    """Deterministic 60-day job history."""
    rng = random.Random(2026)
    rows = []
    fridays = set(_fridays())
    for j in JOBS:
        jid, sysid, scope, sched, (h, mi), typ, dr, iso, ret, mon, enc, dur, size = j
        growth = 1.0
        for k in range(DAYS):
            day = WIN_FROM + timedelta(days=k)
            if sched == WEEKLY and day not in fridays:
                continue
            growth *= 1.0015
            start = datetime(day.year, day.month, day.day, h, mi) + timedelta(minutes=rng.randint(0, 4))
            ev = EVENTS.get((jid, day))
            weekly_full = (day in fridays and 'كامل أسبوعي' in typ)
            d_min = dur * (2.6 if weekly_full else 1.0) * rng.uniform(0.85, 1.2)
            gb = size * growth * (1.0 if (weekly_full or sched == WEEKLY or typ in ('كامل', 'تصدير إعدادات')) else 0.12) * rng.uniform(0.9, 1.1)
            status, msg, ticket = OK, '', ''
            if ev:
                status, msg, ticket, rerun = ev
                if status == FAIL:
                    d_min = rng.uniform(4, 25)
                    gb = 0
                else:
                    gb *= 0.7
            end = start + timedelta(minutes=d_min)
            rows.append(dict(job=jid, sys=sysid, day=day, start=start, end=end, minutes=round(d_min),
                             gb=round(gb, 1), status=status, msg=msg, ticket=ticket, manual=''))
            if ev and ev[3]:
                rh, rm = ev[3]
                rs = datetime(day.year, day.month, day.day, rh, rm)
                if rs < start:
                    rs += timedelta(days=1)
                rd = dur * rng.uniform(0.9, 1.1)
                rows.append(dict(job=jid, sys=sysid, day=rs.date(), start=rs, end=rs + timedelta(minutes=rd),
                                 minutes=round(rd), gb=round(size * growth * (0.12 if sched == DAILY and typ not in ('كامل',) else 1) * rng.uniform(0.9, 1.1), 1),
                                 status=OK, msg='تشغيل يدوي بعد معالجة التذكرة', ticket=ev[2], manual='نعم'))
    rows.sort(key=lambda r: (r['start'], r['job']))
    return rows


def metrics():
    H = history()
    m = {'history': H, 'rows': len(H)}
    per = {}
    for j in JOBS:
        jid = j[0]
        rs = [r for r in H if r['job'] == jid]
        succ_times = [r['start'] for r in rs if r['status'] == OK]
        succ_or_part = [r['start'] for r in rs if r['status'] in (OK, PART)]

        def maxgap(ts, ends=False):
            ts = sorted(ts)
            g = [((b - a).total_seconds() / 3600, a, b) for a, b in zip(ts, ts[1:])]
            if not g:
                return None
            best = max(g)
            return best if ends else best[0]
        crit = SYS[j[1]]['crit']
        unsucc = [r for r in rs if r['status'] in (FAIL, PART)]
        no_ticket = [r for r in unsucc if not r['ticket']]
        rpo = TARGETS[j[1]][0]
        per[jid] = dict(job=j, runs=len(rs), ok=sum(r['status'] == OK for r in rs),
                        part=sum(r['status'] == PART for r in rs), fail=sum(r['status'] == FAIL for r in rs),
                        manual=sum(r['manual'] == 'نعم' for r in rs), unsucc=unsucc, no_ticket=no_ticket,
                        ticket_required=crit in POLICY['ticket_required'], crit=crit,
                        maxgap=maxgap(succ_times), maxgap_lenient=maxgap(succ_or_part), rpo=rpo,
                        rpo_job=jid not in IMAGE_JOBS, gap_ends=maxgap(succ_or_part, True),
                        max_gb=max(r['gb'] for r in rs),
                        rpo_breach=(jid not in IMAGE_JOBS and maxgap(succ_or_part) > rpo + RPO_TOL_H),
                        ret_req=POLICY['retention'][crit], ret=j[8],
                        iso_req=crit in POLICY['isolated_required'], iso=j[7] != 'لا')
    m['per'] = per
    m['total_runs'] = len(H)
    m['total_ok'] = sum(r['status'] == OK for r in H)
    sched = [r for r in H if r['manual'] != 'نعم']
    m['sched_runs'] = len(sched)
    m['sched_ok'] = sum(r['status'] == OK for r in sched)
    # coverage per system
    cov = {}
    for sid, s in SYS.items():
        jobs = [j for j in JOBS if j[1] == sid]
        tests = sorted([t for t in RESTORE_TESTS if t['sys'] == sid], key=lambda t: t['d'])
        last = tests[-1] if tests else None
        interval = POLICY['test_interval_days'].get(s['crit'])
        age = (WIN_TO - last['d']).days if last else None
        cov[sid] = dict(sys=s, jobs=jobs, rpo=TARGETS[sid][0], rto=TARGETS[sid][1], last=last, age=age,
                        interval=interval,
                        test_in_time=(None if interval is None else (last is not None and age <= interval)),
                        met_rto=(None if not last else last['actual'] <= last['rto'] * 60))
    m['cov'] = cov
    m['critical'] = [sid for sid, s in SYS.items() if s['crit'] == 'حرج']
    m['no_job'] = [sid for sid in SYS if not cov[sid]['jobs']]
    return m
