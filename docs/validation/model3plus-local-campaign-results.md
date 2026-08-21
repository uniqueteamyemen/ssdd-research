# نتائج الحملة المحلية لـSSDD Model 3+: حزم الأدلة A–E

**الحالة:** Accepted — دليل سلوكي وسلامة مرجعي محلي فقط.  
**وسم التنفيذ:** `model3plus-local-20260822T020000Z`.  
**قرار النطاق:** لا تتضمن هذه الحملة أي قياس latency أو jitter أو throughput أو overhead، ولا تنفيذ gem5/KVM أو Timing CPU أو FPGA أو CXL Type-3 فعلي، ولا تصلح للاستدلال على أي من تلك المجالات.

## الملخص التنفيذي

أنتجت الحملة سجلاً جديداً لا يكتب فوق خط الأساس المجمد. تحققت النتائج من الترتيب الحتمي، واحتواء الأعطال الممثلة، وتحويرات السجل المعرفة، ومقارنة إعادة التشغيل بين مرجع Python ومرجع Rust محفوظ، وحالة proof-control مترجمة محلياً. اجتازت جميع حالات القبول والرفض المعرفة مسبقاً، وحُفظت **26 مادة خرج خام** في قائمة SHA-256 تحققت لاحقاً بنجاح. [1] [2]

> هذه نتائج لنموذج مرجعي وبرنامج مرجعي مترجم محلياً. إنها ليست نتيجة أداء، وليست دليلاً على CXL أو عتاد أو نظام موزع أو أمان تشغيلي أو جاهزية إنتاجية.

## النتائج حسب الحزمة

| الحزمة | النتيجة المقبولة | الدليل المحفوظ | حد التفسير |
|---|---|---|---|
| **A — المصفوفة الوظيفية الخصومية** | بقي ترتيب **48 حزمة** متطابقاً عبر **128 permutation**؛ رُفض اصطدام four-key الكامل. كما رُفضت حالات `packet_drop` و`node_delay` و`aggregator_failure` و`corrupted_state_ledger` من دون commit جديد، مع حفظ آخر حالة صالحة عند epoch 11. | `ordering.json`، `ordering-chain-stress.json`، `faults.json`، `fault-recovery.json`، `replay-independent.json`. | نموذج reference أحادي العملية؛ لا fault injection شبكي أو تخزيني أو موزع. |
| **B — سلامة السجل وproof** | اكتُشف تحوير `state_hash` و`previous_hash` و`aggregate` و`epoch_id`. قُبل positive control بـ35 عملية، ورُفض `proof-corruption` عند record 18 مع exit code 2. | `ledger-tamper.json`، `proof-accepted.txt`، `proof-corruption.txt`. | برنامج proof-control مترجم محلياً؛ ليس تشغيل gem5 أو SimCXL أو CXL فعلي. |
| **C — إعادة التشغيل عبر مرجعين** | تطابقت Python وRust عبر **100 epoch** وكل hash-chain، وانتهتا إلى `34b7958a64082c326ba3a7cab44468ae9564c7ec2072f88533e10426e23f65c2`. | `python-ledger.json`، `rust-ledger.json`، `cross-language.json`. | Rust comparator مرجع محفوظ ضيق، لا runtime خارجي supplied أو implementation production. |
| **D — الفصل بين المجالات** | ثبت جدول عدم انتقال الدليل بين native reference وgem5 وSimCXL وRTL وFPGA وCXL Type-3 الحقيقي. | خطة الحملة المحلية وسجل التشغيل. | لا تنتقل أي نتيجة إلى مجال آخر لم ينفذ. |
| **E — سجل القطع والأصل** | نجح فحص SHA-256 لكل المواد الخام، ونجح فحص self-hash لقائمة التجزئات. | `run-manifest.txt`، `source-register.sha256`، `SHA256SUMS`، `SHA256SUMS.sha256`. | يحفظ provenance وسلامة الملفات؛ لا يحول النتيجة إلى دليل أعلى نطاقاً. |

## ضبط الجودة وسلامة الأثر

أظهرت المحاولة الأولى (`model3plus-local-20260822T010000Z`) خللاً في ترتيب الإنهاء داخل runner: أضيفت علامة `completed_utc` إلى `run-manifest.txt` بعد حساب SHA-256، ولذلك فشل فحص تجزئة ذلك الملف. لم تُحذف تلك المخرجات. صُحح ترتيب runner بحيث تدخل علامة الإكمال قبل تجميد قائمة التجزئات، ثم شُغلت الحملة من جديد في مجلد جديد مستقل. اجتازت الحملة الثانية فحص كل الملفات وفحص self-hash؛ وهذا هو السجل المعتمد أعلاه.

هذه الواقعة **حلّتها** إعادة التشغيل المنفصلة والتحقق اللاحق. لا تمثل مشكلة قائمة في السجل المعتمد، ولا تغير نتائج الاختبارات السلوكية أو حدودها.

## ما تحققه النتائج وما لا تحققه

| الادعاء | الحالة بعد الحملة | السبب |
|---|---|---|
| ترتيب canonical والسجل الحتمي في النطاق المرجعي المعلن | **Verified** | مخرجات permutation وreplay وhash-chain محفوظة ومتحقق منها. |
| اكتشاف تحويرات السجل وحفظ آخر حالة صالحة في حالات fault الممثلة | **Verified** | حالات الرفض والتعافي المعلنة محفوظة في المخرجات الخام. |
| تطابق Python/Rust reference chain | **Verified** | chain كامل من 100 epoch متطابق، مع حد المرجع-إلى-مرجع. |
| latency أو jitter أو throughput أو overhead | **Open / not measured** | لا KVM أو Timing CPU أو paired baseline/SSDD measurement. |
| gem5/KVM-accelerated execution | **Open / not executed** | `/dev/kvm` غير متاح في سجل التشغيل؛ الحملة لا تدعي بديل Atomic CPU. |
| calibrated CXL Type-3 emulator أو physical CXL Type-3 | **Open / not executed** | لم تشغل الحملة SimCXL ولا عتاد CXL. |
| FPGA synthesis أو board validation | **Open / not executed** | لا bitstream أو timing closure أو board access. |

## الأثر على تأطير Model 3+

تدعم هذه الحملة النسخة **evidence-bounded behavioral validation** من تأطير Model 3+. ولا تدعم النسخة الكمية التي تتحدث عن قياسات الأداء أو `gem5/KVM-accelerated syscall-emulation`. يظل الانتقال إلى توصيف كمي للمحاكاة مشروطاً بقبول بيئة KVM، ثم boot/fast-forward بـKVM والقياس داخل region معلن على Timing CPU، مع manifests متطابقة بين baseline وSSDD وحفظ مخرجات القياس الخام. [3]

## المواد المحفوظة

السجل المنسق محفوظ في [`evidence/prehardware/model3plus-local-20260822T020000Z/`](../../evidence/prehardware/model3plus-local-20260822T020000Z/). وهو يتضمن المخرجات الخام، وسجل المصدر، وملف البيئة، وملفات التحقق، وقائمتي SHA-256. لا يستبدل هذا السجل خط الأساس `prehardware-baseline-v0.1.1` ولا يوسع حدوده. [2]

## المراجع

[1]: [خطة حملة Model 3+ المحلية](model3plus-local-campaign-plan.md) — حزم A–E وحدود المجالات.  
[2]: [إصدار خط الأساس قبل العتاد](prehardware-baseline-release.md) — قاعدة عدم الكتابة فوق السجل المجمد والاحتفاظ بسجل جديد.  
[3]: [/home/ubuntu/ssdd-kvm-measurement-plan.md](/home/ubuntu/ssdd-kvm-measurement-plan.md) — بوابة KVM وTiming CPU للقياسات الكمية.  
