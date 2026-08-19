#!/usr/bin/env python3
"""Собирает uz/index.html из index.html — заменой текста, без копипасты разметки.

Структура, стили, карта и картинки берутся из русской страницы, поэтому любая
правка вёрстки делается один раз. После правки текста на русском — прогнать
скрипт заново:

    python3 build-uz.py

Если строка на русском изменилась, а пара здесь не обновлена, скрипт упадёт
с указанием, что именно не нашлось. Это защита от молчаливого рассинхрона.
"""
import re, pathlib, sys

SRC = pathlib.Path('index.html')
DST = pathlib.Path('uz/index.html')

# (что заменить, на что, сколько раз ожидаем встретить)
PAIRS = [
    # ---------- служебное ----------
    ('<link rel="preload" href="fonts/fira-sans-condensed-700-cyrillic.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="fonts/fira-sans-400-cyrillic.woff2" as="font" type="font/woff2" crossorigin>',
     '<link rel="preload" href="../fonts/fira-sans-condensed-700-latin.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="../fonts/fira-sans-400-latin.woff2" as="font" type="font/woff2" crossorigin>', 1),

    # ---------- отчего случается засор ----------
    ('Отчего случается засор канализации', 'Kanalizatsiya tiqilishi nimadan boʻladi', 1),
    ('Причина определяет способ прочистки, поэтому диспетчер и спрашивает, что именно происходит. Вот четыре сценария, которые мы разбираем чаще всего в Ташкенте.',
     'Sabab tozalash usulini belgilaydi, shuning uchun dispetcher nima boʻlayotganini soʻraydi. Toshkentda eng koʻp uchraydigan toʻrtta holat.', 1),
    ('Жир на стенках', 'Devordagi yogʻ', 1),
    ('Самая частая причина в квартирах и кафе. Жир остывает в трубе и год за годом нарастает слоями, просвет сужается до пальца. Тросом такой налёт только пробивается насквозь — снимает его гидродинамика.',
     'Kvartira va kafelarda eng koʻp uchraydigan sabab. Yogʻ quvurda soviydi va yildan yilga qatlam boʻlib oʻsadi, teshik barmoqdek qoladi. Tros bunday qatqaloqni faqat teshib oʻtadi — uni gidrodinamika olib tashlaydi.', 1),
    ('Тряпки и салфетки', 'Latta va salfetkalar', 1),
    ('Влажные салфетки не растворяются, а сбиваются в плотный жгут и цепляются за стык или поворот. Дальше на них наматывается всё остальное. Достаём тросом с насадкой-крюком.',
     'Nam salfetkalar erimaydi, zich jgutga aylanib, ulanish yoki burilishga ilashadi. Keyin ularga qolgani oʻraladi. Ilmoqli tros bilan chiqaramiz.', 1),
    ('Корни деревьев', 'Daraxt ildizlari', 1),
    ('Беда частных дворов: корень находит трещину в трубе и прорастает внутрь целой бородой. Срезаем фрезой, но потом стоит посмотреть камерой — раз корень зашёл, труба уже повреждена.',
     'Xususiy hovlilarning muammosi: ildiz quvurdagi yoriqni topib, ichkariga soqoldek oʻsib kiradi. Frеza bilan kesamiz, keyin kamera bilan koʻrgan maʼqul — ildiz kirgan boʻlsa, quvur allaqachon shikastlangan.', 1),
    ('Просадка и обвал трубы', 'Quvurning choʻkishi va oʻpirilishi', 1),
    ('Здесь засор — только следствие: труба просела, в яме копится осадок. Прочистка даёт неделю-другую, потом всё повторяется. Такое видно только на видеодиагностике, и решать надо земляными работами.',
     'Bu yerda tiqilish — faqat oqibat: quvur choʻkkan, chuqurchada choʻkma yigʻiladi. Tozalash bir-ikki haftaga yetadi, keyin hammasi takrorlanadi. Buni faqat videodiagnostika koʻrsatadi, yer ishlari bilan hal qilinadi.', 1),
    ('<html lang="ru">', '<html lang="uz">', 1),
    ('<title>Засор канализации в Ташкенте — устраним в день вызова · Аварийная</title>',
     '<title>Toshkentda kanalizatsiya tiqilishi — chaqiruv kuni bartaraf etamiz · Avariynaya</title>', 1),
    ('content="Устраним засор канализации в Ташкенте в день вызова. Аварийная служба круглосуточно, бригада за 40 минут. Прочистка тросом и гидродинамикой, оплата после работы."',
     'content="Toshkentda kanalizatsiya tiqilishini chaqiruv kuni bartaraf etamiz. Avariya xizmati kechayu kunduz, brigada 40 daqiqada. Tros va gidrodinamika bilan tozalash, toʻlov ish tugagach."', 1),
    ('<link rel="canonical" href="https://avariynaya.uz/">',
     '<link rel="canonical" href="https://avariynaya.uz/uz/">', 1),
    ('<meta property="og:locale" content="ru_RU">',
     '<meta property="og:locale" content="uz_UZ">', 1),
    ('content="Засор канализации в Ташкенте — устраним в день вызова"',
     'content="Toshkentda kanalizatsiya tiqilishi — chaqiruv kuni bartaraf etamiz"', 1),
    ('content="Аварийная прочистка засора канализации в Ташкенте и области. Выезд 24/7, приезд за 40 минут, оплата после работы."',
     'content="Toshkent va viloyatda kanalizatsiya tiqilishini avariya tozalash. 24/7 chiqamiz, 40 daqiqada yetib boramiz, toʻlov ish tugagach."', 1),
    ('<meta property="og:url" content="https://avariynaya.uz/">',
     '<meta property="og:url" content="https://avariynaya.uz/uz/">', 1),
    ('<meta property="og:site_name" content="Аварийная">',
     '<meta property="og:site_name" content="Avariynaya">', 1),
    ('<meta property="og:image:alt" content="Мастер аварийной службы у машины с барабаном высокого давления, телефон +998 33 794-70-30">',
     '<meta property="og:image:alt" content="Avariya xizmati ustasi yuqori bosimli barabanli mashina yonida, telefon +998 33 794-70-30">', 1),

    # ---------- переключатель языка ----------
    ('<p class="lang" role="group" aria-label="Язык сайта">\n        <span class="lang__on" aria-current="true">RU</span><a class="lang__off" href="/uz/" hreflang="uz" lang="uz">UZ</a>\n      </p>',
     '<p class="lang" role="group" aria-label="Sayt tili">\n        <a class="lang__off" href="/" hreflang="ru" lang="ru">RU</a><span class="lang__on" aria-current="true">UZ</span>\n      </p>', 1),

    # ---------- шапка ----------
    ('<div class="brand__name">Аварийная</div>', '<div class="brand__name">Avariynaya</div>', 1),
    ('Аварийная служба · Ташкент', 'Avariya xizmati · Toshkent', 1),
    ('Диспетчер на линии', 'Dispetcher aloqada', 1),
    ('aria-label="Позвонить"', 'aria-label="Qoʻngʻiroq qilish"', 1),

    # ---------- первый экран ----------
    ('Выезд 24/7 · 40 минут', '24/7 chiqamiz · 40 daqiqa', 1),
    ('Устраним засор<br>канализации<br>в день вызова', 'Chaqiruv kuni<br>kanalizatsiya<br>tiqilishini yechamiz', 1),
    ('Вода не уходит, запах, стоки в подвале, переполненный септик. Ташкент и область: частные дома, кафе, магазины, махаллинские сети. Гидродинамика, видеодиагностика, откачка.',
     'Suv ketmayapti, hid keladi, oqova yertoʻlada, septik toʻlib ketgan. Toshkent va viloyat: xususiy uylar, kafelar, doʻkonlar, mahalla tarmoqlari. Gidrodinamika, videodiagnostika, soʻrib olish.', 1),
    ('Позвонить сейчас', 'Hozir qoʻngʻiroq qiling', 1),
    ('Услуги и цены</a>', 'Xizmatlar va narxlar</a>', 1),
    ('<span>Оплата после работы</span><span>Гарантия 6 месяцев</span><span>Без вскрытия пола</span>',
     '<span>Toʻlov ish tugagach</span><span>6 oy kafolat</span><span>Polni buzmasdan</span>', 1),

    # ---------- цифры ----------
    ('aria-label="Служба в цифрах"', 'aria-label="Xizmat raqamlarda"', 1),
    ('<span class="stat__unit"> МИН</span>', '<span class="stat__unit"> DAQ</span>', 1),
    ('средний приезд по городу', 'shahar boʻylab oʻrtacha yetib borish', 1),
    ('ночью, в выходные и праздники', 'tunda, dam olish va bayram kunlari', 1),
    ('своих машин, без посредников', 'oʻz mashinamiz, vositachisiz', 1),
    ('<span class="stat__unit"> ЛЕТ</span>', '<span class="stat__unit"> YIL</span>', 1),
    ('работаем в Ташкенте', 'Toshkentda ishlaymiz', 1),

    # ---------- услуги ----------
    ('<h2 class="h2" id="services">Услуги и цены</h2>',
     '<h2 class="h2" id="services">Xizmatlar va narxlar</h2>', 1),
    ('Точную сумму диспетчер называет по телефону — она зависит от диаметра трубы и характера засора. Доплат на месте не бывает.',
     'Aniq summani dispetcher telefonda aytadi — u quvur diametri va tiqilish turiga bogʻliq. Joyida qoʻshimcha toʻlov boʻlmaydi.', 1),

    ('Прочистка засора канализации', 'Kanalizatsiya tiqilishini tozalash', 1),
    ('Кухня, санузел, стояк, наружная линия. Троса или гидродинамика — подбираем по ситуации.',
     'Oshxona, hammom, stoyak, tashqi liniya. Tros yoki gidrodinamika — vaziyatga qarab tanlaymiz.', 1),
    ('от 250 000 сум', '250 000 soʻmdan', 1),

    ('Откачка септика и ям', 'Septik va chohlarni soʻrib olish', 1),
    ('Вакуумные машины 4 и 10 м³. Вывоз и утилизация на официальный полигон.',
     '4 va 10 m³ vakuum mashinalar. Rasmiy poligonga olib chiqib tashlaymiz.', 1),
    ('от 350 000 сум / рейс', '350 000 soʻmdan / reys', 1),

    ('Гидродинамическая промывка', 'Gidrodinamik yuvish', 1),
    ('Давление до 200 бар: жир, ил, корни, отложения. Для кафе и длинных наружных линий.',
     '200 bargacha bosim: yogʻ, loyqa, ildiz, qatqaloq. Kafelar va uzun tashqi liniyalar uchun.', 1),
    ('от 600 000 сум', '600 000 soʻmdan', 1),

    ('Видеодиагностика трубы', 'Quvur videodiagnostikasi', 1),
    ('Камера показывает трещины, провалы и точное место засора. Запись отдаём заказчику.',
     'Kamera yoriq, choʻkish va tiqilishning aniq joyini koʻrsatadi. Yozuvni buyurtmachiga beramiz.', 1),
    ('от 400 000 сум', '400 000 soʻmdan', 1),

    ('Договор для бизнеса', 'Biznes uchun shartnoma', 1),
    ('Кафе, ТЦ, автомойки, пекарни. Плановая чистка жироуловителей, приоритетный выезд.',
     'Kafe, savdo markazlari, avtomoykalar, nonvoyxonalar. Yogʻ tutgichlarni rejali tozalash, navbatsiz chiqish.', 1),
    ('<p class="card__price">по договору</p>', '<p class="card__price">shartnoma boʻyicha</p>', 1),

    ('Не знаете, что нужно?', 'Nima kerakligini bilmayapsizmi?', 1),
    ('Опишите проблему по телефону — подскажем решение и цену за две минуты.',
     'Muammoni telefonda ayting — ikki daqiqada yechim va narxni aytamiz.', 1),

    # ---------- звоните, если ----------
    ('<h2 class="h2" id="cases">Звоните, если</h2>',
     '<h2 class="h2" id="cases">Qoʻngʻiroq qiling, agar</h2>', 1),
    ('Вода уходит медленно или стоит в раковине и душе',
     'suv sekin ketsa yoki rakovina va dushda turib qolsa', 1),
    ('Запах из труб в квартире или во дворе',
     'kvartirada yoki hovlida quvurdan hid kelsa', 1),
    ('Стоки поднимаются в колодце или подтапливают подвал',
     'oqova quduqda koʻtarilsa yoki yertoʻlani bossa', 1),
    ('Септик переполнен, а ассенизатор не приезжает',
     'septik toʻlib ketgan, assenizator esa kelmayotgan boʻlsa', 1),

    # ---------- как проходит вызов ----------
    ('Как проходит вызов', 'Chaqiruv qanday oʻtadi', 1),
    ('<h3 class="step__title">Звонок</h3>', '<h3 class="step__title">Qoʻngʻiroq</h3>', 1),
    ('Спрашиваем адрес и что происходит. Называем вилку цены и время приезда.',
     'Manzil va nima boʻlganini soʻraymiz. Narx oraligʻi va yetib borish vaqtini aytamiz.', 1),
    ('Выезд бригады', 'Brigada chiqadi', 1),
    ('Мастер звонит перед выездом и когда подъезжает. Осмотр на месте бесплатный.',
     'Usta chiqishdan oldin va yetib kelganda qoʻngʻiroq qiladi. Joyida koʻrik bepul.', 1),
    ('<h3 class="step__title">Работа</h3>', '<h3 class="step__title">Ish</h3>', 1),
    ('Прочистка без вскрытия пола и стен. Убираем за собой, показываем результат.',
     'Pol va devorni buzmasdan tozalaymiz. Orqamizdan yigʻishtiramiz, natijani koʻrsatamiz.', 1),
    ('Оплата и гарантия', 'Toʻlov va kafolat', 1),
    ('Платите после работы: наличными, картой или перечислением. Гарантия 6 месяцев.',
     'Ish tugagach toʻlaysiz: naqd, karta yoki pul oʻtkazma orqali. 6 oy kafolat.', 1),

    # ---------- галерея ----------
    ('Работы и техника', 'Ishlar va texnika', 1),
    ('Фото с выездов: что было до, что стало после, и чем работаем.',
     'Chiqishlardan olingan suratlar: avval qanday edi, keyin qanday boʻldi va nima bilan ishlaymiz.', 1),
    ('alt="Мастер аварийной службы в рабочей форме у сервисной машины"',
     'alt="Avariya xizmati ustasi ish kiyimida servis mashinasi yonida"', 1),
    ('alt="Установка гидродинамической промывки: барабан со шлангом, насос и манометр"',
     'alt="Gidrodinamik yuvish qurilmasi: shlangli baraban, nasos va manometr"', 1),
    ('alt="Камера для диагностики трубы: барабан с кабелем, головка с подсветкой и монитор"',
     'alt="Quvur diagnostikasi kamerasi: kabelli baraban, yoritgichli kallak va monitor"', 1),
    ('alt="Двое мастеров промывают наружную линию через открытый колодец во дворе"',
     'alt="Ikki usta hovlidagi ochiq quduq orqali tashqi liniyani yuvmoqda"', 1),
    ('alt="Два среза чугунной трубы: слева просвет забит коростой, справа чистый полный диаметр"',
     'alt="Choʻyan quvurning ikki kesimi: chapda teshik qatqaloqqa toʻlgan, oʻngda toza toʻliq diametr"', 1),
    ('alt="Оператор заводит рукав вакуумной машины в открытый люк септика"',
     'alt="Operator vakuum mashina shlangini septik lyugiga tushirmoqda"', 1),
    ('alt="Мастер чистит жироуловитель в кухне кафе после закрытия"',
     'alt="Usta kafe oshxonasida yopilgandan keyin yogʻ tutgichni tozalamoqda"', 1),
    ('alt="Бригада выгружает барабан со шлангом и ящики из машины ночью у дома"',
     'alt="Brigada tunda uy oldida mashinadan shlangli baraban va yashiklarni tushirmoqda"', 1),

    # ---------- отзывы ----------
    ('Отзывы заказчиков', 'Buyurtmachilar fikri', 1),
    ('Позвонила в 11 вечера, приехали через сорок минут. Стояк в частном доме пробили за час, цену не подняли.',
     'Kechki 11 da qoʻngʻiroq qildim, qirq daqiqada yetib kelishdi. Xususiy uydagi stoyakni bir soatda ochishdi, narxni oshirishmadi.', 1),
    ('Дилноза, Юнусабад', 'Dilnoza, Yunusobod', 1),
    ('Обслуживают жироуловитель в нашем кафе по договору. Раз в месяц, без напоминаний, кухня не встаёт.',
     'Kafemizdagi yogʻ tutgichga shartnoma asosida xizmat koʻrsatishadi. Oyiga bir marta, eslatmasdan, oshxona toʻxtamaydi.', 1),
    ('Тимур, кафе на Мирзо-Улугбек', 'Timur, Mirzo Ulugʻbekdagi kafe', 1),
    ('Другие предлагали копать двор. Здесь сначала запустили камеру, нашли обвал в одном месте — обошлись без раскопок.',
     'Boshqalar hovlini kovlashni taklif qilgandi. Bu yerda avval kamera tushirishdi, bir joyda choʻkish topishdi — kovlamasdan hal boʻldi.', 1),
    ('Сардор, Кибрай', 'Sardor, Qibray', 1),

    # ---------- география ----------
    ('Куда выезжаем', 'Qayerlarga chiqamiz', 1),
    ('Все районы Ташкента и область. За выезд внутри города не доплачиваете.',
     'Toshkentning barcha tumanlari va viloyat. Shahar ichida chiqish uchun qoʻshimcha toʻlamaysiz.', 1),
    ('Область: Кибрай, Зангиата, Чирчик', 'Viloyat: Qibray, Zangiota, Chirchiq', 1),
    ('aria-label="Схема Ташкента: выезжаем во все двенадцать районов города"',
     'aria-label="Toshkent sxemasi: shaharning oʻn ikki tumaniga ham chiqamiz"', 1),
    ('Весь город — все 12 районов. Границы: данные OpenStreetMap (ODbL)',
     'Butun shahar — barcha 12 tuman. Chegaralar: OpenStreetMap maʼlumotlari (ODbL)', 1),
    # названия районов — встречаются дважды: тегом и в <title> внутри карты
    ('Юнусабад', 'Yunusobod', 2), ('Мирзо-Улугбек', 'Mirzo Ulugʻbek', 2),
    ('Яшнабад', 'Yashnobod', 2), ('Чиланзар', 'Chilonzor', 2),
    ('Сергели', 'Sergeli', 2), ('Шайхантахур', 'Shayxontohur', 2),
    ('Бектемир', 'Bektemir', 2), ('Мирабад', 'Mirobod', 2),
    ('Яккасарай', 'Yakkasaroy', 2), ('Учтепа', 'Uchtepa', 2),
    ('Алмазар', 'Olmazor', 2), ('Янгихаёт', 'Yangihayot', 2),

    # ---------- вопросы ----------
    ('Частые вопросы', 'Koʻp beriladigan savollar', 1),
    ('Сколько ждать приезда?', 'Yetib kelishni qancha kutish kerak?', 1),
    ('По городу обычно 40–60 минут, в область — до двух часов. Диспетчер сразу скажет реальное время по вашему адресу.',
     'Shahar boʻylab odatda 40–60 daqiqa, viloyatga — ikki soatgacha. Dispetcher manzilingiz boʻyicha aniq vaqtni darrov aytadi.', 1),
    ('Работаете ночью и в праздники?', 'Tunda va bayramlarda ishlaysizmi?', 1),
    ('Да, круглосуточно. Ночной тариф выше на 20%, о нём предупреждаем до выезда.',
     'Ha, kechayu kunduz. Tungi tarif 20% qimmat, bu haqda chiqishdan oldin ogohlantiramiz.', 1),
    ('Придётся ломать пол или стену?', 'Pol yoki devorni buzish kerak boʻladimi?', 1),
    ('В большинстве случаев нет. Заходим через ревизию или колодец, при сомнениях сначала смотрим камерой.',
     'Koʻp hollarda yoʻq. Reviziya yoki quduq orqali kiramiz, shubha boʻlsa avval kamera bilan koʻramiz.', 1),
    ('Что если засор появится снова?', 'Tiqilish yana paydo boʻlsa-chi?', 1),
    ('В течение 6 месяцев приезжаем повторно бесплатно, если проблема на том же участке.',
     '6 oy ichida oʻsha joyda muammo takrorlansa, bepul qayta chiqamiz.', 1),

    # ---------- финал и подвал ----------
    ('Засор не подождёт до утра', 'Tiqilish tonggacha kutmaydi', 1),
    ('Один звонок — диспетчер назовёт цену и отправит ближайшую бригаду.',
     'Bitta qoʻngʻiroq — dispetcher narxni aytadi va eng yaqin brigadani yuboradi.', 1),
    ('Диспетчеры и мастера говорят по-узбекски и по-русски · оплата наличными, Click, Payme, юрлицам по перечислению',
     'Dispetcher va ustalar oʻzbek va rus tilida gaplashadi · naqd, Click, Payme, yuridik shaxslarga pul oʻtkazma orqali', 1),
    ('«Аварийная» · Ташкент и Ташкентская область · ru / uz',
     '«Avariynaya» · Toshkent va Toshkent viloyati · ru / uz', 1),
    ('Сайт и продвижение — ', 'Sayt va reklama — ', 1),
    ('Круглосуточно · <a href="tel:', 'Kechayu kunduz · <a href="tel:', 1),
]

# микроразметка целиком — проще заменить блоком, чем по кусочкам
LD_UZ = '''[{
  "@context":"https://schema.org",
  "@type":"Plumber",
  "@id":"https://avariynaya.uz/#business",
  "name":"Avariynaya",
  "description":"Toshkent va Toshkent viloyatida kanalizatsiya tozalash avariya xizmati: tiqilishni tozalash, gidrodinamik yuvish, quvur videodiagnostikasi, septik soʻrib olish. Kechayu kunduz chiqamiz.",
  "url":"https://avariynaya.uz/uz/",
  "telephone":"+998337947030",
  "priceRange":"250 000 soʻmdan",
  "inLanguage":"uz",
  "address":{
    "@type":"PostalAddress",
    "addressLocality":"Toshkent",
    "addressCountry":"UZ"
  },
  "areaServed":[
    {"@type":"City","name":"Toshkent"},
    {"@type":"AdministrativeArea","name":"Toshkent viloyati"}
  ],
  "availableLanguage":["uz","ru"],
  "openingHoursSpecification":[{
    "@type":"OpeningHoursSpecification",
    "dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens":"00:00","closes":"23:59"
  }],
  "hasOfferCatalog":{
    "@type":"OfferCatalog","name":"Xizmatlar",
    "itemListElement":[
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Kanalizatsiya tiqilishini tozalash"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Septik va chohlarni soʻrib olish"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Gidrodinamik yuvish"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Quvur videodiagnostikasi"}},
      {"@type":"Offer","itemOffered":{"@type":"Service","name":"Biznes uchun xizmat shartnomasi"}}
    ]
  }
},{
  "@context":"https://schema.org",
  "@type":"FAQPage",
  "inLanguage":"uz",
  "mainEntity":[
    {"@type":"Question","name":"Yetib kelishni qancha kutish kerak?","acceptedAnswer":{"@type":"Answer","text":"Shahar boʻylab odatda 40–60 daqiqa, viloyatga — ikki soatgacha. Dispetcher manzilingiz boʻyicha aniq vaqtni darrov aytadi."}},
    {"@type":"Question","name":"Tunda va bayramlarda ishlaysizmi?","acceptedAnswer":{"@type":"Answer","text":"Ha, kechayu kunduz. Tungi tarif 20% qimmat, bu haqda chiqishdan oldin ogohlantiramiz."}},
    {"@type":"Question","name":"Pol yoki devorni buzish kerak boʻladimi?","acceptedAnswer":{"@type":"Answer","text":"Koʻp hollarda yoʻq. Reviziya yoki quduq orqali kiramiz, shubha boʻlsa avval kamera bilan koʻramiz."}},
    {"@type":"Question","name":"Tiqilish yana paydo boʻlsa-chi?","acceptedAnswer":{"@type":"Answer","text":"6 oy ichida oʻsha joyda muammo takrorlansa, bepul qayta chiqamiz."}},
    {"@type":"Question","name":"Kanalizatsiya tiqilishi nimadan boʻladi?","acceptedAnswer":{"@type":"Answer","text":"Koʻpincha bu quvur devoridagi yogʻ, nam salfetka va lattalar, xususiy hovlilarda daraxt ildizlari yoki quvurning choʻkishi. Sabab tozalash usulini belgilaydi: yogʻni gidrodinamika oladi, lattani tros chiqaradi, ildizni freza kesadi, choʻkishni esa faqat videodiagnostika koʻrsatadi."}}
  ]
}]'''


def main():
    s = SRC.read_text(encoding='utf-8')

    # микроразметку меняем первой: её текст пересекается с текстом страницы
    s, n = re.subn(r'(<script type="application/ld\+json">)\n.*?\n(</script>)',
                   lambda m: m.group(1) + '\n' + LD_UZ + '\n' + m.group(2),
                   s, count=1, flags=re.S)
    if n != 1:
        sys.exit('не найден блок микроразметки')

    problems = []
    for ru, uz, times in PAIRS:
        found = s.count(ru)
        if found != times:
            problems.append(f'  {found} вместо {times}: {ru[:70]}')
            continue
        s = s.replace(ru, uz)
    if problems:
        sys.exit('строки не совпали с русской страницей:\n' + '\n'.join(problems))

    # картинки лежат уровнем выше
    s = s.replace('="img/', '="../img/').replace(', img/', ', ../img/')
    s = s.replace('url(fonts/', 'url(../fonts/')

    if 'Ё' in s or re.search(r'[а-яА-Я]{3,}', re.sub(r'<style>.*?</style>|<!--.*?-->', '', s, flags=re.S)):
        left = set(re.findall(r'[А-Яа-яЁё][А-Яа-яЁё -]{2,}',
                              re.sub(r'<style>.*?</style>|<!--.*?-->', '', s, flags=re.S)))
        sys.exit('на узбекской странице остался русский текст:\n  ' + '\n  '.join(sorted(left)[:20]))

    DST.parent.mkdir(exist_ok=True)
    DST.write_text(s, encoding='utf-8')
    print(f'{DST} собран, {len(s.encode())/1024:.0f} КБ, заменено пар: {len(PAIRS)}')


if __name__ == '__main__':
    main()
