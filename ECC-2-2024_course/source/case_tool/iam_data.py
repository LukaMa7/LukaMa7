# -*- coding: utf-8 -*-
"""Fictional identity & access data for application 01 (and the entity summary)."""
from datetime import datetime as D

# Categories
U, ADM, CADM, BG, SVC, WL, CTR = ('مستخدم عادي', 'مشرف أنظمة (صلاحيات هامة)', 'مشرف مستأجر سحابي (بشري)',
                                  'حساب طوارئ (Break-glass)', 'حساب خدمة (غير بشري)',
                                  'هوية تطبيق/حمل عمل (غير بشري)', 'متعاقد')
HUMAN = {U: 'نعم', ADM: 'نعم', CADM: 'نعم', BG: 'نعم (للطوارئ فقط)', SVC: 'لا', WL: 'لا', CTR: 'نعم'}

ENF, RO, NA = 'مفروضة', 'وضع التقرير فقط', 'لا تنطبق'
EX_TMP, EX_BG = 'مستثنى (GRP-MFA-Temp-Exclusion)', 'مستثنى (GRP-BreakGlass)'
NA_SYNC = 'لا تنطبق (حساب محلي غير متزامن مع السحابة)'
NA_WL = 'لا تنطبق (هوية غير بشرية)'

# account fields:
# id, display, category, owner, unit/company, source, privileged, role, remote, methods, CA01, CA02, VPN, PAM,
# exception, last sign-in, status, priv_ad_group
A = []


def acc(i, disp, cat, owner, unit, src, priv, role, remote, methods, ca01, ca02, vpn, pam, exc, last, status,
        adgrp=False):
    A.append(dict(id=i, disp=disp, cat=cat, owner=owner, unit=unit, src=src, priv=priv, role=role,
                  remote=remote, methods=methods, ca01=ca01, ca02=ca02, vpn=vpn, pam=pam, exc=exc,
                  last=last, status=status, adgrp=adgrp))


SYNC, CLOUD, LOCAL = 'الدليل النشط + متزامن مع السحابة', 'المستأجر السحابي فقط', 'الدليل النشط فقط'
WEB = 'البريد والتطبيقات السحابية من خارج الشبكة'
ON, OFF = 'مفعّل', 'معطّل'

# --- regular users (sample)
acc('u.abdulilah', 'عبدالإله المرزوقي', U, 'عبدالإله المرزوقي', 'مكتب الرئيس التنفيذي', SYNC, 'لا', 'مستخدم', WEB + '؛ VPN', 'رسالة نصية SMS', EX_TMP, NA, ENF, NA, '', D(2026, 9, 1, 8, 30), ON)
acc('u.reem.h', 'ريم الحربي', U, 'ريم الحربي', 'الإدارة العامة للأمن السيبراني', SYNC, 'لا', 'مستخدم', WEB + '؛ VPN', 'تطبيق المصادقة', ENF, NA, ENF, NA, '', D(2026, 9, 29, 9, 2), ON)
acc('u.asma.f', 'أسماء الفيفي', U, 'أسماء الفيفي', 'الإدارة العامة للأمن السيبراني', SYNC, 'لا', 'مستخدم', WEB, 'تطبيق المصادقة', ENF, NA, NA, NA, '', D(2026, 9, 28, 13, 40), ON)
acc('u.noura.k', 'نورة القحطاني', U, 'نورة القحطاني', 'الإدارة العامة للمالية', SYNC, 'لا', 'مستخدم ERP (محاسب)', WEB, 'تطبيق المصادقة', ENF, NA, NA, NA, '', D(2026, 9, 30, 10, 15), ON)
acc('u.waleed.m', 'وليد المطيري', U, 'وليد المطيري', 'الإدارة العامة للمالية', SYNC, 'لا', 'مستخدم ERP (معتمد أوامر صرف)', WEB + '؛ VPN', 'تطبيق المصادقة', ENF, NA, ENF, NA, '', D(2026, 8, 20, 21, 5), OFF + ' (2026-08-21 08:40)')
acc('u.hanan.s', 'حنان السبيعي', U, 'حنان السبيعي', 'إدارة خدمة المستفيدين (مركز الاتصال)', SYNC, 'لا', 'مستخدم', WEB, 'رسالة نصية SMS', ENF, NA, NA, NA, '', D(2026, 9, 30, 8, 1), ON)
acc('u.yazeed.a', 'يزيد العتيبي', U, 'يزيد العتيبي', 'الإدارة العامة للموارد البشرية', SYNC, 'لا', 'مستخدم نظام الموارد البشرية', WEB, 'تطبيق المصادقة', ENF, NA, NA, NA, '', D(2026, 9, 29, 11, 20), ON)
acc('u.maha.t', 'مها التميمي', U, 'مها التميمي', 'إدارة الوثائق والخدمات المشتركة', SYNC, 'لا', 'مستخدم نظام الوثائق', WEB, 'تطبيق المصادقة', ENF, NA, NA, NA, '', D(2026, 9, 23, 12, 10), ON)
acc('u.ali.z', 'علي الزهراني', U, 'علي الزهراني', 'وكالة الخدمات الرقمية', SYNC, 'لا', 'مستخدم', WEB + '؛ VPN', 'تطبيق المصادقة', ENF, NA, ENF, NA, '', D(2026, 9, 27, 19, 33), ON)
acc('u.salem.o', 'سالم العمري', U, 'سالم العمري', 'الإدارة القانونية', SYNC, 'لا', 'مستخدم', WEB, 'رسالة نصية SMS', ENF, NA, NA, NA, '', D(2026, 9, 24, 9, 45), ON)
acc('u.dalia.r', 'داليا الرويلي', U, 'داليا الرويلي', 'إدارة المشتريات والعقود', SYNC, 'لا', 'مستخدم ERP (مشتريات)', WEB, 'تطبيق المصادقة', ENF, NA, NA, NA, '', D(2026, 9, 30, 12, 5), ON)
acc('u.khalid.sh', 'خالد الشمري', U, 'خالد الشمري', 'الإدارة العامة للمالية', SYNC, 'لا', 'مالك أعمال ERP', WEB + '؛ VPN', 'تطبيق المصادقة', ENF, NA, ENF, NA, '', D(2026, 9, 30, 14, 12), ON)
acc('u.muneera.d', 'منيرة الدوسري', U, 'منيرة الدوسري', 'الإدارة العامة للموارد البشرية', SYNC, 'لا', 'مالك أعمال نظام الموارد البشرية', WEB, 'تطبيق المصادقة', ENF, NA, NA, NA, '', D(2026, 9, 29, 8, 50), ON)
# --- privileged on-prem admins (separate admin accounts, used only through PAM)
PAMONLY = 'لا يوجد مباشرة (عبر بوابة PAM فقط)'
acc('adm.sultan', 'حساب إدارة — م. سلطان الغامدي', ADM, 'م. سلطان الغامدي', 'الإدارة العامة لتقنية المعلومات', LOCAL, 'نعم', 'Domain Admins', PAMONLY, 'مفتاح أمان FIDO2', NA_SYNC, NA, NA, ENF, '', D(2026, 9, 29, 10, 4), ON, True)
acc('adm.badr', 'حساب إدارة — بدر القرني', ADM, 'بدر القرني', 'الإدارة العامة لتقنية المعلومات', LOCAL, 'نعم', 'Domain Admins', PAMONLY, 'مفتاح أمان FIDO2', NA_SYNC, NA, NA, ENF, '', D(2026, 9, 30, 9, 15), ON, True)
acc('adm.fahad', 'حساب إدارة — م. فهد العنزي', ADM, 'م. فهد العنزي', 'الإدارة العامة لتقنية المعلومات', LOCAL, 'نعم', 'Domain Admins؛ Enterprise Admins', PAMONLY, 'مفتاح أمان FIDO2', NA_SYNC, NA, NA, ENF, '', D(2026, 6, 30, 16, 20), ON, True)
acc('adm.hisham', 'حساب إدارة — هشام البلوي', ADM, 'هشام البلوي', 'الإدارة العامة لتقنية المعلومات', LOCAL, 'نعم', 'Backup Operators؛ Server-Admins', PAMONLY, 'مفتاح أمان FIDO2', NA_SYNC, NA, NA, ENF, '', D(2026, 9, 28, 9, 14), ON, True)
acc('adm.omar', 'حساب إدارة — م. عمر الحازمي', ADM, 'م. عمر الحازمي', 'الإدارة العامة لتقنية المعلومات', LOCAL, 'نعم', 'Network-Admins', PAMONLY, 'مفتاح أمان FIDO2', NA_SYNC, NA, NA, ENF, '', D(2026, 9, 25, 20, 45), ON, True)
acc('adm.lama', 'حساب إدارة — م. لمى السبيعي', ADM, 'م. لمى السبيعي', 'الإدارة العامة لتقنية المعلومات', LOCAL, 'نعم', 'Server-Admins (خوادم التطبيقات)', PAMONLY, 'تطبيق المصادقة', NA_SYNC, NA, NA, ENF, '', D(2026, 9, 22, 11, 2), ON, True)
# --- human cloud tenant admins (cloud-only accounts)
ADMP = 'بوابة الإدارة السحابية والبريد من أي موقع'
acc('cadm.badr', 'مشرف سحابي — بدر القرني', CADM, 'بدر القرني', 'الإدارة العامة لتقنية المعلومات', CLOUD, 'نعم', 'مدير عام المستأجر (Global Administrator)', ADMP, 'تطبيق المصادقة؛ مفتاح أمان FIDO2', ENF, RO, NA, NA, '', D(2026, 9, 30, 15, 40), ON)
acc('cadm.fahad', 'مشرف سحابي — م. فهد العنزي', CADM, 'م. فهد العنزي', 'الإدارة العامة لتقنية المعلومات', CLOUD, 'نعم', 'مدير عام المستأجر (Global Administrator)', ADMP, 'لا يوجد', ENF, RO, NA, NA, '', D(2026, 9, 21, 9, 31), ON)
acc('cadm.sultan', 'مشرف سحابي — م. سلطان الغامدي', CADM, 'م. سلطان الغامدي', 'الإدارة العامة لتقنية المعلومات', CLOUD, 'نعم', 'مدير خدمة البريد (Exchange Administrator)', ADMP, 'رسالة نصية SMS', ENF, RO, NA, NA, '', D(2026, 9, 24, 10, 30), ON)
acc('cadm.lama', 'مشرف سحابي — م. لمى السبيعي', CADM, 'م. لمى السبيعي', 'الإدارة العامة لتقنية المعلومات', CLOUD, 'نعم', 'مدير التطبيقات (Application Administrator)', ADMP, 'تطبيق المصادقة', EX_TMP, RO, NA, NA, '', D(2026, 8, 25, 21, 40), ON)
acc('cadm.majed', 'مشرف سحابي — م. ماجد الزهراني', CADM, 'م. ماجد الزهراني', 'الإدارة العامة للأمن السيبراني', CLOUD, 'نعم', 'مدير الأمن (Security Administrator)', ADMP, 'تطبيق المصادقة', ENF, RO, NA, NA, '', D(2026, 9, 26, 10, 5), ON)
# --- break-glass
acc('bg.emergency01', 'حساب طوارئ 1', BG, 'م. نوال الشهري (حفظ المفتاح في الخزنة)', 'الإدارة العامة للأمن السيبراني', CLOUD, 'نعم', 'مدير عام المستأجر (Global Administrator)', 'يُستخدم في الطوارئ فقط', 'مفتاح أمان FIDO2 (محفوظ في الخزنة)', EX_BG, EX_BG, NA, NA, 'EXC-2026-004', D(2026, 6, 28, 10, 0), ON)
acc('bg.emergency02', 'حساب طوارئ 2', BG, 'م. نوال الشهري (حفظ المفتاح في الخزنة)', 'الإدارة العامة للأمن السيبراني', CLOUD, 'نعم', 'مدير عام المستأجر (Global Administrator)', 'يُستخدم في الطوارئ فقط', 'مفتاح أمان FIDO2 (محفوظ في الخزنة)', EX_BG, EX_BG, NA, NA, 'EXC-2026-004', D(2026, 6, 28, 10, 20), ON)
# --- service accounts (non-human, AD)
acc('svc.backup', 'حساب خدمة النسخ الاحتياطي', SVC, 'هشام البلوي', 'الإدارة العامة لتقنية المعلومات', LOCAL, 'نعم', 'Domain Admins (لتشغيل وكلاء النسخ)', 'لا يوجد', 'كلمة مرور فقط', NA_SYNC, NA, NA, NA, '', D(2026, 9, 30, 1, 0), ON, True)
acc('svc.sql.erp', 'حساب خدمة قاعدة بيانات ERP', SVC, 'م. لمى السبيعي', 'الإدارة العامة لتقنية المعلومات', LOCAL, 'لا', 'تشغيل خدمة قاعدة البيانات', 'لا يوجد', 'كلمة مرور فقط', NA_SYNC, NA, NA, NA, '', D(2026, 9, 30, 0, 5), ON)
acc('svc.dirsync', 'حساب مزامنة الدليل مع السحابة', SVC, 'بدر القرني', 'الإدارة العامة لتقنية المعلومات', LOCAL, 'نعم', 'صلاحية نسخ بيانات الدليل (Replicate Directory Changes)', 'لا يوجد', 'كلمة مرور فقط', NA_SYNC, NA, NA, NA, '', D(2026, 9, 30, 23, 30), ON, True)
acc('svc.scanner', 'حساب خدمة فحص الثغرات', SVC, 'م. ماجد الزهراني', 'الإدارة العامة للأمن السيبراني', LOCAL, 'نعم', 'مشرف محلي على الخوادم (للفحص المصادق)', 'لا يوجد', 'كلمة مرور فقط (لا تنتهي)', NA_SYNC, NA, NA, NA, 'EXC-2026-011', D(2026, 9, 27, 2, 0), ON)
acc('svc.print', 'حساب خدمة الطباعة', SVC, 'م. سلطان الغامدي', 'الإدارة العامة لتقنية المعلومات', LOCAL, 'لا', 'تشغيل خدمة الطباعة', 'لا يوجد', 'كلمة مرور فقط', NA_SYNC, NA, NA, NA, '', D(2026, 9, 30, 7, 0), ON)
# --- workload identities (cloud app registrations)
acc('app-portal-api', 'هوية تطبيق واجهات البوابة', WL, 'م. لمى السبيعي', 'الإدارة العامة لتقنية المعلومات', CLOUD, 'لا', 'قراءة/كتابة حاوية تخزين البوابة فقط', 'غير تفاعلي (من بيئة الاستضافة)', 'شهادة رقمية (تنتهي 2027-04-30)', NA_WL, NA_WL, NA, NA, '', D(2026, 9, 30, 23, 55), ON)
acc('app-mobile-notify', 'هوية خدمة إشعارات التطبيق', WL, 'م. لمى السبيعي', 'الإدارة العامة لتقنية المعلومات', CLOUD, 'لا', 'إرسال الإشعارات فقط', 'غير تفاعلي (من بيئة الاستضافة)', 'شهادة رقمية (تنتهي 2027-05-10)', NA_WL, NA_WL, NA, NA, '', D(2026, 9, 30, 23, 58), ON)
acc('app-erp-mail', 'هوية تكامل ERP مع البريد', WL, 'م. لمى السبيعي', 'الإدارة العامة لتقنية المعلومات', CLOUD, 'نعم', 'إرسال البريد باسم أي صندوق في الجهة (Mail.Send لجميع الصناديق)', 'غير تفاعلي (من خادم ERP)', 'سر عميل Client secret (أُنشئ 2026-01-15، ينتهي 2027-01-15)', NA_WL, NA_WL, NA, NA, '', D(2026, 9, 30, 22, 10), ON)
acc('app-siem-connector', 'هوية موصل SIEM', WL, 'م. ماجد الزهراني', 'الإدارة العامة للأمن السيبراني', CLOUD, 'لا', 'قراءة سجلات التدقيق والدخول فقط', 'غير تفاعلي (من منصة SIEM)', 'سر عميل Client secret (أُنشئ 2026-03-01، ينتهي 2027-03-01)', NA_WL, NA_WL, NA, NA, '', D(2026, 9, 30, 23, 50), ON)
# --- contractors (sample)
acc('ctr.dev.yousef', 'يوسف القرشي (متعاقد)', CTR, 'م. لمى السبيعي (مشرف العقد)', 'الواحة الرقمية', SYNC, 'لا', 'مطور — بيئة الاختبار', WEB + '؛ VPN', 'رسالة نصية SMS', EX_TMP, NA, ENF, NA, '', D(2026, 9, 4, 19, 52), ON)
acc('ctr.dev.rana', 'رنا الأحمدي (متعاقدة)', CTR, 'م. لمى السبيعي (مشرف العقد)', 'الواحة الرقمية', SYNC, 'لا', 'مطورة — بيئة الاختبار', WEB + '؛ VPN', 'تطبيق المصادقة', ENF, NA, ENF, NA, '', D(2026, 9, 29, 17, 10), ON)
acc('ctr.dev.ammar', 'عمار الحربي (متعاقد سابق)', CTR, 'م. لمى السبيعي (مشرف العقد)', 'الواحة الرقمية', SYNC, 'لا', 'مطور', WEB + '؛ VPN', 'تطبيق المصادقة', ENF, NA, ENF, NA, '', D(2026, 7, 31, 16, 40), OFF + ' (2026-07-31 17:05)')
acc('ctr.soc.fares', 'فارس الدوسري (متعاقد)', CTR, 'م. ماجد الزهراني (مشرف العقد)', 'نطاق اليقظة', SYNC, 'نعم', 'محلل — صلاحية إدارة قواعد الكشف في SIEM', 'VPN', 'تطبيق المصادقة', ENF, NA, ENF, NA, '', D(2026, 9, 30, 21, 4), ON)
acc('ctr.soc.nawaf', 'نواف الشهراني (متعاقد)', CTR, 'م. ماجد الزهراني (مشرف العقد)', 'نطاق اليقظة', SYNC, 'لا', 'محلل — قراءة فقط في SIEM', 'VPN', 'تطبيق المصادقة', ENF, NA, ENF, NA, '', D(2026, 9, 30, 6, 12), ON)
acc('ctr.soc.samer', 'سامر الغامدي (متعاقد سابق)', CTR, 'م. ماجد الزهراني (مشرف العقد)', 'نطاق اليقظة', SYNC, 'لا', 'محلل', 'VPN', 'تطبيق المصادقة', ENF, NA, ENF, NA, '', D(2026, 9, 1, 8, 2), OFF + ' (2026-09-01 09:10)')
acc('ctr.host.ziyad', 'زياد المالكي (متعاقد)', CTR, 'م. لمى السبيعي (مشرف العقد)', 'سحابة الأفق', SYNC, 'لا', 'دعم الاستضافة — بريد وتذاكر فقط', WEB, 'تطبيق المصادقة', ENF, NA, NA, NA, '', D(2026, 9, 18, 10, 0), ON)
acc('ctr.bks.mazen', 'مازن العنزي (متعاقد)', CTR, 'هشام البلوي (مشرف العقد)', 'أرشيف الحصين', SYNC, 'لا', 'دعم التخزين المعزول', 'VPN', 'تطبيق المصادقة', ENF, NA, ENF, NA, '', D(2026, 9, 27, 18, 5), ON)

ACC = {a['id']: a for a in A}

# ---------------------------------------------------------------- policies
POLICIES = [
    dict(id='CA01', name='فرض التحقق متعدد العوامل للوصول من خارج شبكة الجهة', state=ENF,
         include='جميع المستخدمين', exclude='GRP-BreakGlass؛ GRP-MFA-Temp-Exclusion',
         apps='جميع التطبيقات السحابية', cond='الموقع: خارج نطاقات IP الموثوقة للجهة', clients='المتصفح؛ تطبيقات الجوال والحاسب الحديثة',
         grant='اشتراط التحقق متعدد العوامل (أي طريقة مسجلة)', modified='2026-03-15', by='cadm.badr'),
    dict(id='CA02', name='فرض التحقق متعدد العوامل لأدوار الإدارة في المستأجر السحابي', state=RO,
         include='أدوار الإدارة (Global/Exchange/Application/Security Administrator)؛ GRP-Cloud-Admins', exclude='GRP-BreakGlass',
         apps='جميع التطبيقات السحابية', cond='أي موقع', clients='المتصفح؛ تطبيقات الجوال والحاسب الحديثة',
         grant='اشتراط التحقق متعدد العوامل (أي طريقة مسجلة)', modified='2026-06-10', by='cadm.badr'),
]

GROUPS = [
    ('GRP-BreakGlass', 'حسابات الطوارئ', 'bg.emergency01؛ bg.emergency02', '2026-02-01', 'م. نوال الشهري'),
    ('GRP-MFA-Temp-Exclusion', 'استثناء مؤقت خلال ترحيل البريد السحابي', 'u.abdulilah؛ cadm.lama؛ ctr.dev.yousef', '2026-03-15', 'cadm.badr'),
    ('GRP-Cloud-Admins', 'مشرفو المستأجر السحابي', 'cadm.badr؛ cadm.fahad؛ cadm.sultan؛ cadm.lama؛ cadm.majed', '2025-12-02', 'بدر القرني'),
    ('Domain Admins', 'مجموعة مشرفي النطاق (الدليل النشط)', 'adm.sultan؛ adm.badr؛ adm.fahad؛ svc.backup', 'افتراضية في النظام', 'بدر القرني'),
    ('Enterprise Admins', 'مشرفو الغابة (الدليل النشط)', 'adm.fahad', 'افتراضية في النظام', 'بدر القرني'),
    ('Backup Operators', 'مشغلو النسخ الاحتياطي', 'adm.hisham', 'افتراضية في النظام', 'بدر القرني'),
    ('Server-Admins', 'مشرفو الخوادم', 'adm.hisham؛ adm.lama', '2024-05-19', 'م. سلطان الغامدي'),
    ('Network-Admins', 'مشرفو أجهزة الشبكة وجدران الحماية', 'adm.omar', '2024-05-19', 'م. سلطان الغامدي'),
    ('صلاحية Replicate Directory Changes', 'صلاحية نسخ بيانات الدليل (لأداة المزامنة)', 'svc.dirsync', '2025-11-30', 'بدر القرني'),
    ('GRP-VPN-Users', 'المخولون بالدخول عن بعد عبر VPN', '143 عضواً (موظفون ومتعاقدون)', '2023-02-11', 'م. عمر الحازمي'),
]

EXCEPTIONS = [
    ('EXC-2025-019', 'ملف VPN قديم لمورد سابق دون تحقق متعدد', 'م. نوال الشهري', '2025-08-01', '2025-10-31', 'قائمة IP محددة', 'مغلق (أُلغي الملف 2025-10-30)'),
    ('EXC-2026-004', 'استثناء مجموعة GRP-BreakGlass من سياسات الوصول المشروط CA01 وCA02', 'م. نوال الشهري', '2026-02-01', '2026-12-31 (استثناء دائم يراجع سنوياً حسب البند 4.4)', 'مفتاحا FIDO2 في خزنة؛ تنبيه فوري في SIEM عند أي دخول؛ اختبار ربع سنوي موثق', 'سارٍ'),
    ('EXC-2026-011', 'حساب svc.scanner بكلمة مرور لا تنتهي', 'م. نوال الشهري', '2026-08-01', '2026-10-29', 'كلمة مرور من 30 حرفاً في خزنة؛ منع الدخول التفاعلي على الحساب', 'سارٍ'),
]

# ---------------------------------------------------------------- sign-in log (sample)
CLOUD_LOG, VPN_LOG, PAM_LOG = 'المنصة السحابية', 'بوابة VPN', 'بوابة PAM'
INT, EXT, ADMNET, VIAVPN = 'داخل الشبكة', 'خارج الشبكة', 'الشبكة الإدارية', 'عبر VPN'
SF = 'كلمة مرور فقط (عامل واحد)'
S = []  # each: dt, account, source, resource, kind, client, ip, location, method, ca, result


def si(t, a, src, res, kind, client, ip, loc, method, ca, result):
    S.append(dict(t=t, a=a, src=src, res=res, kind=kind, client=client, ip=ip, loc=loc, method=method, ca=ca,
                  result=result))


TI = 'تفاعلي'
si(D(2026, 7, 5, 8, 12), 'u.reem.h', CLOUD_LOG, 'البريد عبر الويب', TI, 'متصفح', '10.20.14.22', INT, SF, 'لم تنطبق CA01 (داخل الشبكة)', 'نجاح')
si(D(2026, 7, 6, 21, 30), 'u.reem.h', VPN_LOG, 'الشبكة الداخلية', TI, 'عميل VPN', '198.51.100.61', EXT, 'كلمة مرور + تطبيق المصادقة', 'تحقق VPN متعدد العوامل: مفروض', 'نجاح')
si(D(2026, 7, 12, 9, 5), 'adm.sultan', PAM_LOG, 'خادم ERP-APP01', 'تفاعلي (جلسة إدارة)', 'بوابة PAM', '10.20.50.21', ADMNET, 'كلمة مرور + مفتاح FIDO2', 'تحقق PAM متعدد العوامل: مفروض', 'نجاح')
si(D(2026, 7, 19, 2, 14), 'u.hanan.s', CLOUD_LOG, 'البريد عبر الويب', TI, 'متصفح', '192.0.2.77', EXT, 'كلمة مرور صحيحة — رُفض العامل الثاني', 'CA01: مفروضة — لم يكتمل التحقق', 'فشل')
si(D(2026, 7, 19, 2, 15), 'u.salem.o', CLOUD_LOG, 'البريد عبر الويب', TI, 'متصفح', '192.0.2.77', EXT, 'كلمة مرور خاطئة', '—', 'فشل')
si(D(2026, 7, 23, 10, 40), 'app-portal-api', CLOUD_LOG, 'حاوية تخزين البوابة', 'هوية حمل عمل (غير تفاعلي)', 'بيانات اعتماد العميل', '203.0.113.10', EXT + ' (بيئة الاستضافة)', 'شهادة رقمية', 'لا تنطبق سياسات المستخدمين', 'نجاح')
si(D(2026, 8, 3, 11, 20), 'ctr.soc.fares', VPN_LOG, 'الشبكة الداخلية', TI, 'عميل VPN', '198.51.100.140', EXT, 'كلمة مرور + تطبيق المصادقة', 'تحقق VPN متعدد العوامل: مفروض', 'نجاح')
si(D(2026, 8, 3, 11, 26), 'ctr.soc.fares', 'منصة SIEM', 'وحدة تحكم SIEM', TI, 'متصفح عبر VPN', '10.30.0.15', VIAVPN, 'كلمة مرور (ضمن جلسة VPN متحقق منها)', '—', 'نجاح')
si(D(2026, 8, 9, 22, 47), 'cadm.majed', CLOUD_LOG, 'بوابة الإدارة السحابية', TI, 'متصفح', '198.51.100.88', EXT, 'كلمة مرور + تطبيق المصادقة', 'CA01: مفروضة — مستوفاة؛ CA02: وضع التقرير — مستوفاة', 'نجاح')
si(D(2026, 8, 12, 7, 55), 'svc.sql.erp', 'سجل أحداث خادم ERP-DB01', 'قاعدة بيانات ERP', 'خدمة (غير تفاعلي)', 'Kerberos', '10.20.40.11', INT, 'كلمة مرور الحساب', '—', 'نجاح')
si(D(2026, 8, 17, 23, 14), 'cadm.sultan', CLOUD_LOG, 'البريد الإلكتروني (IMAP)', TI, 'عميل بريد قديم — IMAP بالتحقق الأساسي (Basic)', '203.0.113.45', EXT, SF, 'لم تُطبق أي سياسة (نوع العميل غير مدرج في شروط السياسات)', 'نجاح')
si(D(2026, 8, 18, 2, 7), 'cadm.sultan', CLOUD_LOG, 'البريد الإلكتروني (IMAP)', TI, 'عميل بريد قديم — IMAP بالتحقق الأساسي (Basic)', '203.0.113.45', EXT, SF, 'لم تُطبق أي سياسة (نوع العميل غير مدرج في شروط السياسات)', 'نجاح')
si(D(2026, 8, 20, 21, 5), 'u.waleed.m', CLOUD_LOG, 'البريد عبر الويب', TI, 'متصفح', '198.51.100.203', EXT, 'كلمة مرور + تطبيق المصادقة', 'CA01: مفروضة — مستوفاة', 'نجاح')
si(D(2026, 8, 25, 21, 40), 'cadm.lama', CLOUD_LOG, 'بوابة الإدارة السحابية', TI, 'متصفح', '198.51.100.23', EXT, SF, 'CA01: لم تنطبق — المستخدم مستثنى (GRP-MFA-Temp-Exclusion)؛ CA02: وضع التقرير — كانت ستتطلب التحقق متعدد العوامل', 'نجاح')
si(D(2026, 8, 27, 9, 14), 'adm.hisham', PAM_LOG, 'خادم النسخ BKP-SRV01', 'تفاعلي (جلسة إدارة)', 'بوابة PAM', '10.20.50.33', ADMNET, 'كلمة مرور + مفتاح FIDO2', 'تحقق PAM متعدد العوامل: مفروض', 'نجاح')
si(D(2026, 8, 30, 16, 2), 'app-erp-mail', CLOUD_LOG, 'خدمة إرسال البريد', 'هوية حمل عمل (غير تفاعلي)', 'بيانات اعتماد العميل', '203.0.113.200', EXT + ' (عنوان الخروج للجهة)', 'سر عميل', 'لا تنطبق سياسات المستخدمين', 'نجاح')
si(D(2026, 9, 1, 8, 30), 'u.abdulilah', CLOUD_LOG, 'البريد عبر الويب', TI, 'متصفح (جوال)', '198.51.100.17', EXT, SF, 'CA01: لم تنطبق — المستخدم مستثنى (GRP-MFA-Temp-Exclusion)', 'نجاح')
si(D(2026, 9, 3, 10, 12), 'cadm.badr', CLOUD_LOG, 'بوابة الإدارة السحابية', TI, 'متصفح', '10.20.14.31', INT, SF, 'CA02: وضع التقرير — كانت ستتطلب التحقق متعدد العوامل (لم يُفرض)', 'نجاح')
si(D(2026, 9, 4, 19, 40), 'ctr.dev.yousef', VPN_LOG, 'الشبكة الداخلية', TI, 'عميل VPN', '198.51.100.99', EXT, 'كلمة مرور + رسالة نصية', 'تحقق VPN متعدد العوامل: مفروض', 'نجاح')
si(D(2026, 9, 4, 19, 52), 'ctr.dev.yousef', CLOUD_LOG, 'البريد عبر الويب', TI, 'متصفح', '198.51.100.99', EXT, SF, 'CA01: لم تنطبق — المستخدم مستثنى (GRP-MFA-Temp-Exclusion)', 'نجاح')
si(D(2026, 9, 8, 11, 3), 'app-siem-connector', CLOUD_LOG, 'واجهة سجلات التدقيق', 'هوية حمل عمل (غير تفاعلي)', 'بيانات اعتماد العميل', '203.0.113.200', EXT + ' (عنوان الخروج للجهة)', 'سر عميل', 'لا تنطبق سياسات المستخدمين', 'نجاح')
si(D(2026, 9, 10, 14, 25), 'adm.badr', PAM_LOG, 'وحدة تحكم النطاق DC01', 'تفاعلي (جلسة إدارة)', 'بوابة PAM', '10.20.50.18', ADMNET, 'كلمة مرور + مفتاح FIDO2', 'تحقق PAM متعدد العوامل: مفروض', 'نجاح')
si(D(2026, 9, 14, 19, 22), 'svc.backup', 'سجل أحداث خادم BKP-SRV01', 'خادم النسخ BKP-SRV01', 'تفاعلي — سطح المكتب البعيد (RDP، نوع الدخول 10)', 'RDP مباشر (لم يمر عبر PAM)', '10.20.50.114 (PC-IT-114)', ADMNET, SF, '—', 'نجاح')
si(D(2026, 9, 16, 10, 0), 'svc.dirsync', CLOUD_LOG, 'خدمة مزامنة الدليل', 'خدمة (غير تفاعلي)', 'أداة المزامنة', '203.0.113.200', EXT + ' (عنوان الخروج للجهة)', 'كلمة مرور الحساب', 'لا تنطبق', 'نجاح')
si(D(2026, 9, 21, 9, 31), 'cadm.fahad', CLOUD_LOG, 'بوابة الإدارة السحابية', TI, 'متصفح', '10.20.14.40', INT, SF, 'CA02: وضع التقرير — كانت ستتطلب التحقق متعدد العوامل (لم يُفرض)', 'نجاح')
si(D(2026, 9, 22, 3, 12), 'cadm.sultan', CLOUD_LOG, 'بوابة الإدارة السحابية', TI, 'متصفح', '192.0.2.140', EXT, 'كلمة مرور صحيحة — لم يكتمل العامل الثاني', 'CA01: مفروضة — لم يكتمل التحقق', 'فشل')
si(D(2026, 9, 23, 12, 10), 'u.maha.t', CLOUD_LOG, 'البريد عبر الويب', TI, 'متصفح', '10.20.22.9', INT, SF, 'لم تنطبق CA01 (داخل الشبكة)', 'نجاح')
si(D(2026, 9, 25, 20, 45), 'adm.omar', PAM_LOG, 'جدار الحماية FW-CORE', 'تفاعلي (جلسة إدارة)', 'بوابة PAM', '10.20.50.27', ADMNET, 'كلمة مرور + مفتاح FIDO2', 'تحقق PAM متعدد العوامل: مفروض', 'نجاح')
si(D(2026, 9, 27, 18, 5), 'ctr.bks.mazen', VPN_LOG, 'الشبكة الداخلية', TI, 'عميل VPN', '198.51.100.150', EXT, 'كلمة مرور + تطبيق المصادقة', 'تحقق VPN متعدد العوامل: مفروض', 'نجاح')
si(D(2026, 9, 29, 7, 50), 'app-mobile-notify', CLOUD_LOG, 'خدمة الإشعارات', 'هوية حمل عمل (غير تفاعلي)', 'بيانات اعتماد العميل', '203.0.113.11', EXT + ' (بيئة الاستضافة)', 'شهادة رقمية', 'لا تنطبق سياسات المستخدمين', 'نجاح')
si(D(2026, 9, 30, 15, 40), 'cadm.badr', CLOUD_LOG, 'بوابة الإدارة السحابية', TI, 'متصفح', '198.51.100.70', EXT, 'كلمة مرور + مفتاح FIDO2', 'CA01: مفروضة — مستوفاة؛ CA02: وضع التقرير — مستوفاة', 'نجاح')
S.sort(key=lambda r: r['t'])

# ---------------------------------------------------------------- access review (Q2 2026)
REVIEW = [
    dict(scope='نظام ERP (جميع الحسابات)', reviewer='خالد الشمري (مالك الأعمال)', inscope=212, reviewed=198, remove=9, removed=6,
         status='معتمدة', signed='2026-07-28', note='لم تُراجع حسابات إدارة المشتريات لعدم توفر المراجع في موعد الحملة'),
    dict(scope='نظام الموارد البشرية (جميع الحسابات)', reviewer='منيرة الدوسري (مالك الأعمال)', inscope=64, reviewed=64, remove=3, removed=3,
         status='معتمدة', signed='2026-07-21', note=''),
    dict(scope='المخولون بالدخول عن بعد (GRP-VPN-Users)', reviewer='م. سلطان الغامدي', inscope=143, reviewed=0, remove=None, removed=None,
         status='قيد التنفيذ', signed='', note='لم تكتمل حتى تاريخ الاستخراج'),
    dict(scope='أدوار الإدارة في المستأجر السحابي', reviewer='م. نوال الشهري', inscope=None, reviewed=0, remove=None, removed=None,
         status='لم تبدأ', signed='', note=''),
    dict(scope='مجموعات الصلاحيات الهامة في الدليل النشط', reviewer='م. نوال الشهري', inscope=None, reviewed=None, remove=1, removed=0,
         status='معتمدة', signed='2026-07-30', note='قرار الإزالة: إخراج svc.backup من Domain Admins'),
]
# derive counts that must match the account list
_cloud_admin_members = [a['id'] for a in A if a['cat'] in (CADM, BG)]
_ad_priv_members = [a['id'] for a in A if a['adgrp']]
REVIEW[3]['inscope'] = len(_cloud_admin_members)
REVIEW[4]['inscope'] = len(_ad_priv_members)
REVIEW[4]['reviewed'] = len(_ad_priv_members)

# ---------------------------------------------------------------- leavers (HR) and disable events
LEAVERS = [
    dict(emp='E-10233', name='منصور الحربي', kind='موظف', unit='إدارة خدمة المستفيدين (مركز الاتصال)', reason='استقالة', end=D(2026, 7, 9, 14, 0),
         ad='u.mansour.h', ad_off=D(2026, 7, 9, 14, 22), vpn_off=None, vpn='لا يملك صلاحية VPN', erp='لا يوجد حساب', erp_off=None, ref='HR-REQ-2026-311'),
    dict(emp='C-0418', name='عمار الحربي', kind='متعاقد (الواحة الرقمية)', unit='وكالة الخدمات الرقمية', reason='انتهاء التكليف', end=D(2026, 7, 31, 17, 0),
         ad='ctr.dev.ammar', ad_off=D(2026, 7, 31, 17, 5), vpn_off=D(2026, 7, 31, 17, 5), vpn='نعم', erp='لا يوجد حساب', erp_off=None, ref='HR-REQ-2026-347'),
    dict(emp='E-09871', name='هند السلمي', kind='موظف', unit='إدارة المشتريات والعقود', reason='نقل إلى جهة أخرى', end=D(2026, 8, 6, 13, 30),
         ad='u.hind.s', ad_off=D(2026, 8, 6, 13, 41), vpn_off=D(2026, 8, 6, 13, 45), vpn='نعم', erp='hind.s', erp_off=D(2026, 8, 6, 14, 2), ref='HR-REQ-2026-362'),
    dict(emp='E-10045', name='وليد المطيري', kind='موظف', unit='الإدارة العامة للمالية', reason='إنهاء خدمة', end=D(2026, 8, 20, 15, 0),
         ad='u.waleed.m', ad_off=D(2026, 8, 21, 8, 40), vpn_off=D(2026, 8, 21, 8, 45), vpn='نعم', erp='waleed.m', erp_off=None, ref='HR-REQ-2026-388'),
    dict(emp='C-0433', name='سامر الغامدي', kind='متعاقد (نطاق اليقظة)', unit='الإدارة العامة للأمن السيبراني', reason='استبدال من المورد', end=D(2026, 9, 1, 9, 0),
         ad='ctr.soc.samer', ad_off=D(2026, 9, 1, 9, 10), vpn_off=D(2026, 9, 1, 9, 10), vpn='نعم', erp='لا يوجد حساب', erp_off=None, ref='HR-REQ-2026-402'),
    dict(emp='E-10302', name='لينا القحطاني', kind='موظف', unit='الإدارة العامة للموارد البشرية', reason='استقالة', end=D(2026, 9, 17, 12, 0),
         ad='u.lina.q', ad_off=D(2026, 9, 17, 12, 30), vpn_off=D(2026, 9, 17, 12, 31), vpn='نعم', erp='lina.q', erp_off=D(2026, 9, 17, 12, 50), ref='HR-REQ-2026-421'),
    dict(emp='E-10118', name='ثامر العسيري', kind='موظف', unit='الإدارة العامة للمالية', reason='تقاعد', end=D(2026, 9, 28, 16, 0),
         ad='u.thamer.a', ad_off=D(2026, 9, 28, 16, 20), vpn_off=None, vpn='لا يملك صلاحية VPN', erp='thamer.a', erp_off=D(2026, 9, 28, 16, 45), ref='HR-REQ-2026-437'),
]
ERP_STATUS_0930 = {'waleed.m': 'نشط — الدور: معتمد أوامر الصرف؛ آخر دخول 2026-08-19 16:48',
                   'hind.s': 'معطّل', 'lina.q': 'معطّل', 'thamer.a': 'معطّل'}
LEAVER_SLA_MIN = 60  # entity policy (training assumption) for «مباشرة»


def minutes(a, b):
    return (b - a).total_seconds() / 60.0


def metrics():
    m = {}
    priv = [a for a in A if a['priv'] == 'نعم']
    m['priv'] = priv
    m['priv_human'] = [a for a in priv if a['cat'] in (ADM, CADM, BG, CTR)]
    m['priv_nonhuman'] = [a for a in priv if a['cat'] in (SVC, WL)]
    m['cadm'] = [a for a in A if a['cat'] == CADM]
    m['cadm_registered'] = [a for a in m['cadm'] if a['methods'] != 'لا يوجد']
    m['cadm_none'] = [a for a in m['cadm'] if a['methods'] == 'لا يوجد']
    m['cadm_sms'] = [a for a in m['cadm'] if 'SMS' in a['methods'] and 'FIDO2' not in a['methods'] and 'تطبيق' not in a['methods']]
    m['adm'] = [a for a in A if a['cat'] == ADM]
    m['excluded_tmp'] = [a for a in A if a['ca01'] == EX_TMP]
    m['bg'] = [a for a in A if a['cat'] == BG]
    m['svc'] = [a for a in A if a['cat'] == SVC]
    m['wl'] = [a for a in A if a['cat'] == WL]
    m['total'] = len(A)
    m['by_cat'] = {}
    for a in A:
        m['by_cat'][a['cat']] = m['by_cat'].get(a['cat'], 0) + 1
    # sign-ins: successful, single factor, and (remote or privileged account)
    sf_rows = []
    for r in S:
        a = ACC[r['a']]
        single = r['method'].startswith('كلمة مرور فقط')
        remote = r['loc'].startswith(EXT)
        if r['result'] == 'نجاح' and single and a['cat'] not in (SVC, WL) and (remote or a['priv'] == 'نعم'):
            sf_rows.append(r)
    m['sf_rows'] = sf_rows
    m['legacy_rows'] = [r for r in S if 'IMAP' in r['client']]
    m['report_only_rows'] = [r for r in S if 'كانت ستتطلب' in r['ca']]
    m['svc_interactive'] = [r for r in S if ACC[r['a']]['cat'] == SVC and r['kind'].startswith('تفاعلي')]
    m['signins'] = len(S)
    # leavers
    lv = []
    for L in LEAVERS:
        d_ad = minutes(L['end'], L['ad_off'])
        d_vpn = minutes(L['end'], L['vpn_off']) if L['vpn_off'] else None
        d_erp = minutes(L['end'], L['erp_off']) if L['erp_off'] else None
        erp_active = L['erp'] not in ('لا يوجد حساب',) and L['erp_off'] is None
        late = [x for x in (d_ad, d_vpn, d_erp) if x is not None and x > LEAVER_SLA_MIN]
        lv.append(dict(L=L, d_ad=d_ad, d_vpn=d_vpn, d_erp=d_erp, erp_active=erp_active, late=bool(late) or erp_active))
    m['leavers'] = lv
    m['leavers_bad'] = [x for x in lv if x['late']]
    post_end = [r for r in S for x in m['leavers_bad']
                if r['a'] == x['L']['ad'] and x['L']['end'] <= r['t'] <= x['L']['ad_off'] and r['result'] == 'نجاح']
    m['leaver_post_end'] = post_end
    # review
    tot_in = sum(r['inscope'] for r in REVIEW)
    tot_rev = sum(r['reviewed'] or 0 for r in REVIEW)
    m['rev_in'], m['rev_done'] = tot_in, tot_rev
    m['rev_complete_rows'] = [r for r in REVIEW if r['reviewed'] == r['inscope'] and r['status'] == 'معتمدة']
    m['rev_remove'] = sum(r['remove'] or 0 for r in REVIEW)
    m['rev_removed'] = sum(r['removed'] or 0 for r in REVIEW)
    m['erp_unreviewed'] = REVIEW[0]['inscope'] - REVIEW[0]['reviewed']
    m['cloud_admin_members'] = _cloud_admin_members
    m['ad_priv_members'] = _ad_priv_members
    return m
