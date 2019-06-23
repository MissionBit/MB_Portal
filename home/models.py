from salesforce import models

from django.db import models as mdls 
from django.contrib.auth.models import User as django_user
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(mdls.Model):
    user = mdls.OneToOneField(django_user, on_delete=mdls.CASCADE)
    change_pwd = mdls.BooleanField(default=False)

    @receiver(post_save, sender=django_user)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=django_user)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()        


class Contact(models.Model):
    is_deleted = models.BooleanField(verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
    master_record = models.ForeignKey('self', models.DO_NOTHING, related_name='contact_masterrecord_set', sf_read_only=models.READ_ONLY, blank=True, null=True)
    #account = models.ForeignKey(Account, models.DO_NOTHING, related_name='contact_account_set', blank=True, null=True)  # Master Detail Relationship *
    last_name = models.CharField(max_length=80)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    salutation = models.CharField(max_length=40, choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs.'), ('Dr.', 'Dr.'), ('Prof.', 'Prof.')], blank=True, null=True)
    middle_name = models.CharField(max_length=40, blank=True, null=True)
    suffix = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=121, verbose_name='Full Name', sf_read_only=models.READ_ONLY)
    mailing_street = models.TextField(blank=True, null=True)
    mailing_city = models.CharField(max_length=40, blank=True, null=True)
    mailing_state = models.CharField(max_length=80, verbose_name='Mailing State/Province', blank=True, null=True)
    mailing_postal_code = models.CharField(max_length=20, verbose_name='Mailing Zip/Postal Code', blank=True, null=True)
    mailing_country = models.CharField(max_length=80, blank=True, null=True)
    mailing_state_code = models.CharField(max_length=10, verbose_name='Mailing State/Province Code', choices=[('AC', 'Acre'), ('AG', 'Agrigento'), ('AG', 'Aguascalientes'), ('AL', 'Alabama'), ('AL', 'Alagoas'), ('AK', 'Alaska'), ('AB', 'Alberta'), ('AL', 'Alessandria'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('AN', 'Ancona'), ('AN', 'Andaman and Nicobar Islands'), ('AP', 'Andhra Pradesh'), ('34', 'Anhui'), ('AO', 'Aosta'), ('AR', 'Arezzo'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AR', 'Arunachal Pradesh'), ('AP', 'Ascoli Piceno'), ('AS', 'Assam'), ('AT', 'Asti'), ('ACT', 'Australian Capital Territory'), ('AV', 'Avellino'), ('BA', 'Bahia'), ('BC', 'Baja California'), ('BS', 'Baja California Sur'), ('BA', 'Bari'), ('BT', 'Barletta-Andria-Trani'), ('11', 'Beijing'), ('BL', 'Belluno'), ('BN', 'Benevento'), ('BG', 'Bergamo'), ('BI', 'Biella'), ('BR', 'Bihar'), ('BO', 'Bologna'), ('BZ', 'Bolzano'), ('BS', 'Brescia'), ('BR', 'Brindisi'), ('BC', 'British Columbia'), ('CA', 'Cagliari'), ('CA', 'California'), ('CL', 'Caltanissetta'), ('CM', 'Campeche'), ('CB', 'Campobasso'), ('CI', 'Carbonia-Iglesias'), ('CW', 'Carlow'), ('CE', 'Caserta'), ('CT', 'Catania'), ('CZ', 'Catanzaro'), ('CN', 'Cavan'), ('CE', 'Ceará'), ('CH', 'Chandigarh'), ('CT', 'Chhattisgarh'), ('CS', 'Chiapas'), ('CH', 'Chieti'), ('CH', 'Chihuahua'), ('71', 'Chinese Taipei'), ('50', 'Chongqing'), ('CE', 'Clare'), ('CO', 'Coahuila'), ('CL', 'Colima'), ('CO', 'Colorado'), ('CO', 'Como'), ('CT', 'Connecticut'), ('CO', 'Cork'), ('CS', 'Cosenza'), ('CR', 'Cremona'), ('KR', 'Crotone'), ('CN', 'Cuneo'), ('DN', 'Dadra and Nagar Haveli'), ('DD', 'Daman and Diu'), ('DE', 'Delaware'), ('DL', 'Delhi'), ('DC', 'District of Columbia'), ('DF', 'Distrito Federal'), ('DL', 'Donegal'), ('D', 'Dublin'), ('DG', 'Durango'), ('EN', 'Enna'), ('ES', 'Espírito Santo'), ('DF', 'Federal District'), ('FM', 'Fermo'), ('FE', 'Ferrara'), ('FI', 'Florence'), ('FL', 'Florida'), ('FG', 'Foggia'), ('FC', 'Forlì-Cesena'), ('FR', 'Frosinone'), ('35', 'Fujian'), ('G', 'Galway'), ('62', 'Gansu'), ('GE', 'Genoa'), ('GA', 'Georgia'), ('GA', 'Goa'), ('GO', 'Goiás'), ('GO', 'Gorizia'), ('GR', 'Grosseto'), ('GT', 'Guanajuato'), ('44', 'Guangdong'), ('45', 'Guangxi'), ('GR', 'Guerrero'), ('52', 'Guizhou'), ('GJ', 'Gujarat'), ('46', 'Hainan'), ('HR', 'Haryana'), ('HI', 'Hawaii'), ('13', 'Hebei'), ('23', 'Heilongjiang'), ('41', 'Henan'), ('HG', 'Hidalgo'), ('HP', 'Himachal Pradesh'), ('91', 'Hong Kong'), ('42', 'Hubei'), ('43', 'Hunan'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IM', 'Imperia'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('IS', 'Isernia'), ('JA', 'Jalisco'), ('JK', 'Jammu and Kashmir'), ('JH', 'Jharkhand'), ('32', 'Jiangsu'), ('36', 'Jiangxi'), ('22', 'Jilin'), ('KS', 'Kansas'), ('KA', 'Karnataka'), ('KY', 'Kentucky'), ('KL', 'Kerala'), ('KY', 'Kerry'), ('KE', 'Kildare'), ('KK', 'Kilkenny'), ('AQ', "L'Aquila"), ('LD', 'Lakshadweep'), ('LS', 'Laois'), ('SP', 'La Spezia'), ('LT', 'Latina'), ('LE', 'Lecce'), ('LC', 'Lecco'), ('LM', 'Leitrim'), ('21', 'Liaoning'), ('LK', 'Limerick'), ('LI', 'Livorno'), ('LO', 'Lodi'), ('LD', 'Longford'), ('LA', 'Louisiana'), ('LH', 'Louth'), ('LU', 'Lucca'), ('92', 'Macao'), ('MC', 'Macerata'), ('MP', 'Madhya Pradesh'), ('MH', 'Maharashtra'), ('ME', 'Maine'), ('MN', 'Manipur'), ('MB', 'Manitoba'), ('MN', 'Mantua'), ('MA', 'Maranhão'), ('MD', 'Maryland'), ('MS', 'Massa and Carrara'), ('MA', 'Massachusetts'), ('MT', 'Matera'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MO', 'Mayo'), ('MH', 'Meath'), ('VS', 'Medio Campidano'), ('ML', 'Meghalaya'), ('ME', 'Messina'), ('ME', 'Mexico State'), ('MI', 'Michigan'), ('MI', 'Michoacán'), ('MI', 'Milan'), ('MG', 'Minas Gerais'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MZ', 'Mizoram'), ('MO', 'Modena'), ('MN', 'Monaghan'), ('MT', 'Montana'), ('MB', 'Monza and Brianza'), ('MO', 'Morelos'), ('NL', 'Nagaland'), ('NA', 'Naples'), ('NA', 'Nayarit'), ('NE', 'Nebraska'), ('15', 'Nei Mongol'), ('NV', 'Nevada'), ('NB', 'New Brunswick'), ('NL', 'Newfoundland and Labrador'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NSW', 'New South Wales'), ('NY', 'New York'), ('64', 'Ningxia'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('NT', 'Northern Territory'), ('NT', 'Northwest Territories'), ('NO', 'Novara'), ('NS', 'Nova Scotia'), ('NL', 'Nuevo León'), ('NU', 'Nunavut'), ('NU', 'Nuoro'), ('OA', 'Oaxaca'), ('OR', 'Odisha'), ('OY', 'Offaly'), ('OG', 'Ogliastra'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OT', 'Olbia-Tempio'), ('ON', 'Ontario'), ('OR', 'Oregon'), ('OR', 'Oristano'), ('PD', 'Padua'), ('PA', 'Palermo'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PR', 'Parma'), ('PV', 'Pavia'), ('PA', 'Pennsylvania'), ('PE', 'Pernambuco'), ('PG', 'Perugia'), ('PU', 'Pesaro and Urbino'), ('PE', 'Pescara'), ('PC', 'Piacenza'), ('PI', 'Piauí'), ('PI', 'Pisa'), ('PT', 'Pistoia'), ('PN', 'Pordenone'), ('PZ', 'Potenza'), ('PO', 'Prato'), ('PE', 'Prince Edward Island'), ('PY', 'Puducherry'), ('PB', 'Puebla'), ('PB', 'Punjab'), ('63', 'Qinghai'), ('QC', 'Quebec'), ('QLD', 'Queensland'), ('QE', 'Querétaro'), ('QR', 'Quintana Roo'), ('RG', 'Ragusa'), ('RJ', 'Rajasthan'), ('RA', 'Ravenna'), ('RC', 'Reggio Calabria'), ('RE', 'Reggio Emilia'), ('RI', 'Rhode Island'), ('RI', 'Rieti'), ('RN', 'Rimini'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RM', 'Rome'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('RN', 'Roscommon'), ('RO', 'Rovigo'), ('SA', 'Salerno'), ('SL', 'San Luis Potosí'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SK', 'Saskatchewan'), ('SS', 'Sassari'), ('SV', 'Savona'), ('SE', 'Sergipe'), ('61', 'Shaanxi'), ('37', 'Shandong'), ('31', 'Shanghai'), ('14', 'Shanxi'), ('51', 'Sichuan'), ('SI', 'Siena'), ('SK', 'Sikkim'), ('SI', 'Sinaloa'), ('SO', 'Sligo'), ('SO', 'Sondrio'), ('SO', 'Sonora'), ('SA', 'South Australia'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('SR', 'Syracuse'), ('TB', 'Tabasco'), ('TM', 'Tamaulipas'), ('TN', 'Tamil Nadu'), ('TA', 'Taranto'), ('TAS', 'Tasmania'), ('TN', 'Tennessee'), ('TE', 'Teramo'), ('TR', 'Terni'), ('TX', 'Texas'), ('12', 'Tianjin'), ('TA', 'Tipperary'), ('TL', 'Tlaxcala'), ('TO', 'Tocantins'), ('TP', 'Trapani'), ('TN', 'Trento'), ('TV', 'Treviso'), ('TS', 'Trieste'), ('TR', 'Tripura'), ('TO', 'Turin'), ('UD', 'Udine'), ('UT', 'Utah'), ('UT', 'Uttarakhand'), ('UP', 'Uttar Pradesh'), ('VA', 'Varese'), ('VE', 'Venice'), ('VE', 'Veracruz'), ('VB', 'Verbano-Cusio-Ossola'), ('VC', 'Vercelli'), ('VT', 'Vermont'), ('VR', 'Verona'), ('VV', 'Vibo Valentia'), ('VI', 'Vicenza'), ('VIC', 'Victoria'), ('VA', 'Virginia'), ('VT', 'Viterbo'), ('WA', 'Washington'), ('WD', 'Waterford'), ('WB', 'West Bengal'), ('WA', 'Western Australia'), ('WH', 'Westmeath'), ('WV', 'West Virginia'), ('WX', 'Wexford'), ('WW', 'Wicklow'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'), ('65', 'Xinjiang'), ('54', 'Xizang'), ('YU', 'Yucatán'), ('YT', 'Yukon Territories'), ('53', 'Yunnan'), ('ZA', 'Zacatecas'), ('33', 'Zhejiang')], blank=True, null=True)
    mailing_country_code = models.CharField(max_length=10, default=models.DEFAULTED_ON_CREATE, choices=[('AF', 'Afghanistan'), ('AX', 'Aland Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia, Plurinational State of'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('TW', 'Chinese Taipei'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, the Democratic Republic of the'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', "Cote d'Ivoire"), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CW', 'Curaçao'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'), ('VA', 'Holy See (Vatican City State)'), ('HN', 'Honduras'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran, Islamic Republic of'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', "Korea, Democratic People's Republic of"), ('KR', 'Korea, Republic of'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', "Lao People's Democratic Republic"), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libyan Arab Jamahiriya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MK', 'Macedonia, the former Yugoslav Republic of'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('MD', 'Moldova, Republic of'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PS', 'Palestinian Territory, Occupied'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('QA', 'Qatar'), ('RE', 'Reunion'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('BL', 'Saint Barthélemy'), ('SH', 'Saint Helena, Ascension and Tristan da Cunha'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'), ('MF', 'Saint Martin (French part)'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SX', 'Sint Maarten (Dutch part)'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard and Jan Mayen'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela, Bolivarian Republic of'), ('VN', 'Viet Nam'), ('VG', 'Virgin Islands, British')], blank=True,null=True)
    mobile_phone = models.CharField(max_length=40, blank=True, null=True)
    home_phone = models.CharField(max_length=40, blank=True, null=True)
    other_phone = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    department = models.CharField(max_length=80, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    owner = models.ForeignKey('User', models.DO_NOTHING, related_name='contact_owner_set', blank=True)
    created_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    created_by = models.ForeignKey('User', models.DO_NOTHING, related_name='contact_createdby_set', sf_read_only=models.READ_ONLY)
    last_modified_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    last_modified_by = models.ForeignKey('User', models.DO_NOTHING, related_name='contact_lastmodifiedby_set', sf_read_only=models.READ_ONLY)
    system_modstamp = models.DateTimeField(sf_read_only=models.READ_ONLY)
    last_activity_date = models.DateField(verbose_name='Last Activity', sf_read_only=models.READ_ONLY, blank=True, null=True)
    last_curequest_date = models.DateTimeField(db_column='LastCURequestDate', verbose_name='Last Stay-in-Touch Request Date', sf_read_only=models.READ_ONLY, blank=True, null=True)
    last_cuupdate_date = models.DateTimeField(db_column='LastCUUpdateDate', verbose_name='Last Stay-in-Touch Save Date', sf_read_only=models.READ_ONLY, blank=True, null=True)
    last_viewed_date = models.DateTimeField(sf_read_only=models.READ_ONLY, blank=True, null=True)
    last_referenced_date = models.DateTimeField(sf_read_only=models.READ_ONLY, blank=True, null=True)
    email_bounced_reason = models.CharField(max_length=255, blank=True, null=True)
    email_bounced_date = models.DateTimeField(blank=True, null=True)
    is_email_bounced = models.BooleanField(sf_read_only=models.READ_ONLY, default=False)
    photo_url = models.URLField(verbose_name='Photo URL', sf_read_only=models.READ_ONLY, blank=True, null=True)
    jigsaw_contact_id = models.CharField(max_length=20, verbose_name='Jigsaw Contact ID', sf_read_only=models.READ_ONLY, blank=True, null=True)
    individual = models.ForeignKey('Individual', models.DO_NOTHING, blank=True, null=True)

    class Meta(models.Model.Meta):
        db_table = 'Contact'
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        # keyPrefix = '003'

class User(models.Model):
    username = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    middle_name = models.CharField(max_length=40, blank=True, null=True)
    suffix = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=121, verbose_name='Full Name', sf_read_only=models.READ_ONLY)
    company_name = models.CharField(max_length=80, blank=True, null=True)
    division = models.CharField(max_length=80, blank=True, null=True)
    department = models.CharField(max_length=80, blank=True, null=True)
    title = models.CharField(max_length=80, blank=True, null=True)
    street = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    state = models.CharField(max_length=80, verbose_name='State/Province', blank=True, null=True)
    postal_code = models.CharField(max_length=20, verbose_name='Zip/Postal Code', blank=True, null=True)
    country = models.CharField(max_length=80, blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Active', default=models.DEFAULTED_ON_CREATE)

    class Meta(models.Model.Meta):
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        # keyPrefix = '003'

    def __str__(self):
        if self.is_active:
            active = "Active"
        else:
            active = "Inactive"
        return "%s %s -- %s" % (self.first_name, self.last_name, active)   

class Individual(models.Model):
    owner = models.ForeignKey('User', models.DO_NOTHING, related_name='individual_owner_set')  # Master Detail Relationship *
    is_deleted = models.BooleanField(verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
    last_name = models.CharField(max_length=80)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    salutation = models.CharField(max_length=40, choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs.'), ('Dr.', 'Dr.'), ('Prof.', 'Prof.')], blank=True, null=True)
    middle_name = models.CharField(max_length=40, blank=True, null=True)
    suffix = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=121, sf_read_only=models.READ_ONLY)

    class Meta(models.Model.Meta):
        db_table = 'Individual'
        verbose_name = 'Individual'
        verbose_name_plural = 'Individuals'
        # keyPrefix = '003'

class Account(models.Model):
    is_deleted = models.BooleanField(verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
    master_record = models.ForeignKey('self', models.DO_NOTHING, related_name='account_masterrecord_set', sf_read_only=models.READ_ONLY, blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name='Account Name')
    type = models.CharField(max_length=40, verbose_name='Account Type', choices=[('School', 'School'), ('Foundation', 'Foundation'), ('Government', 'Government'), ('Business', 'Business'), ('Nonprofit', 'Nonprofit')], blank=True, null=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, related_name='account_parent_set', blank=True, null=True)
    billing_street = models.TextField(blank=True, null=True)
    billing_city = models.CharField(max_length=40, blank=True, null=True)
    billing_state = models.CharField(max_length=80, verbose_name='Billing State/Province', blank=True, null=True)
    billing_postal_code = models.CharField(max_length=20, verbose_name='Billing Zip/Postal Code', blank=True, null=True)
    billing_country = models.CharField(max_length=80, blank=True, null=True)
    
    class Meta(models.Model.Meta):
        db_table = 'Account'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        # keyPrefix = '001'

class ClassOffering(models.Model):
    #owner = models.ForeignKey('Group', models.DO_NOTHING)  # Reference to tables [Group, User]
    is_deleted = models.BooleanField(verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
    name = models.CharField(max_length=80, verbose_name='Class Offering Name', default=models.DEFAULTED_ON_CREATE, blank=True, null=True)
    created_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    created_by = models.ForeignKey('User', models.DO_NOTHING, related_name='classoffering_createdby_set', sf_read_only=models.READ_ONLY)
    last_modified_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    last_modified_by = models.ForeignKey('User', models.DO_NOTHING, related_name='classoffering_lastmodifiedby_set', sf_read_only=models.READ_ONLY)
    system_modstamp = models.DateTimeField(sf_read_only=models.READ_ONLY)
    last_viewed_date = models.DateTimeField(sf_read_only=models.READ_ONLY, blank=True, null=True)
    last_referenced_date = models.DateTimeField(sf_read_only=models.READ_ONLY, blank=True, null=True)
    start_date = models.DateField(custom=True, db_column='Start_Date__c', verbose_name='Start Date', blank=True, null=True)
    end_date = models.DateField(custom=True, db_column='End_Date__c', verbose_name='End Date', blank=True, null=True)
    description = models.TextField(custom=True, blank=True, null=True)
    location = models.ForeignKey(Account, models.DO_NOTHING, custom=True, blank=True, null=True)
    course = models.CharField(custom=True, max_length=255, choices=[('Android Game Design', 'Android Game Design'), ('Intro to Web Programming', 'Intro to Web Programming'), ('Field Trips', 'Field Trips'), ('Intro to Game Design with Unity', 'Intro to Game Design with Unity'), ('Web Design 101', 'Web Design 101'), ('Mobile App Dev with Ionic', 'Mobile App Dev with Ionic'), ('MB Internship', 'MB Internship'), ('Structured Study Program', 'Structured Study Program')], blank=True, null=True)
    instructor = models.ForeignKey('Contact', models.DO_NOTHING, custom=True, blank=True, null=True)
    academic_semester = models.CharField(custom=True, db_column='Academic_semester__c', max_length=1300, verbose_name='Academic semester', sf_read_only=models.READ_ONLY, blank=True, null=True)
    meeting_days = models.CharField(custom=True, db_column='Meeting_Days__c', max_length=255, verbose_name='Meeting Days', choices=[('M/W', 'M/W'), ('T/R', 'T/R'), ('M-F', 'M-F')], blank=True, null=True)
    course_short_name = models.CharField(custom=True, db_column='Course_short_name__c', max_length=1300, verbose_name='Course short name', sf_read_only=models.READ_ONLY, blank=True, null=True)
    count_total_female_students = models.DecimalField(custom=True, db_column='Count_total_female_students__c', max_digits=18, decimal_places=0, verbose_name='Count - Total Female Students', sf_read_only=models.READ_ONLY, blank=True, null=True)
    count_total_latino_african_american = models.DecimalField(custom=True, db_column='Count_total_latino_african_american__c', max_digits=18, decimal_places=0, verbose_name='Count - Total African American', sf_read_only=models.READ_ONLY, blank=True, null=True)
    count_total_latino_students = models.DecimalField(custom=True, db_column='Count_Total_Latino_Students__c', max_digits=18, decimal_places=0, verbose_name='Count - Total Latino Students', sf_read_only=models.READ_ONLY, blank=True, null=True)
    female = models.DecimalField(custom=True, max_digits=18, decimal_places=1, verbose_name='% Female', sf_read_only=models.READ_ONLY, blank=True, null=True)
    latino_african_american = models.DecimalField(custom=True, db_column='Latino_African_American__c', max_digits=18, decimal_places=1, verbose_name='% Latino/African American', sf_read_only=models.READ_ONLY, blank=True, null=True)
    current_academic_semester = models.CharField(custom=True, db_column='Current_academic_semester__c', max_length=1300, verbose_name='Current academic semester', sf_read_only=models.READ_ONLY, blank=True, null=True)
    in_current_semester = models.BooleanField(custom=True, db_column='In_current_semester__c', verbose_name='In current semester?', sf_read_only=models.READ_ONLY)
    
    class Meta(models.Model.Meta):
        db_table = 'Class_Offering__c'
        verbose_name = 'Class Offering'
        verbose_name_plural = 'Class Offerings'
        # keyPrefix = 'a0h'

class ClassEnrollment(models.Model):
    is_deleted = models.BooleanField(verbose_name='Deleted', sf_read_only=models.READ_ONLY, default=False)
    name = models.CharField(max_length=80, verbose_name='Class Enrollment #', sf_read_only=models.READ_ONLY)
    created_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    created_by = models.ForeignKey('User', models.DO_NOTHING, related_name='classenrollment_createdby_set', sf_read_only=models.READ_ONLY)
    last_modified_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    last_modified_by = models.ForeignKey('User', models.DO_NOTHING, related_name='classenrollment_lastmodifiedby_set', sf_read_only=models.READ_ONLY)
    system_modstamp = models.DateTimeField(sf_read_only=models.READ_ONLY)
    last_activity_date = models.DateField(sf_read_only=models.READ_ONLY, blank=True, null=True)
    last_viewed_date = models.DateTimeField(sf_read_only=models.READ_ONLY, blank=True, null=True)
    last_referenced_date = models.DateTimeField(sf_read_only=models.READ_ONLY, blank=True, null=True)
    contact = models.ForeignKey('Contact', models.DO_NOTHING, custom=True, related_name='classenrollment_contact_set')  # Master Detail Relationship 0
    role = models.CharField(custom=True, max_length=255, choices=[('Student', 'Student'), ('TA', 'TA'), ('Volunteer', 'Volunteer')], blank=True, null=True)
    class_offering = models.ForeignKey('ClassOffering', models.DO_NOTHING, db_column='Class_Offering__c', custom=True)  # Master Detail Relationship 1
    status = models.CharField(custom=True, max_length=255, choices=[('Applied', 'Applied'), ('Waitlisted', 'Waitlisted'), ('Enrolled', 'Enrolled'), ('Completed-Course', 'Completed-Course'), ('Withdrew-Application', 'Withdrew-Application'), ('Rejected', 'Rejected'), ('Dropped', 'Dropped')], blank=True, null=True)
    in_current_semester = models.BooleanField(custom=True, db_column='In_current_semester__c', verbose_name='In current semester?', sf_read_only=models.READ_ONLY)
    attended_family_orientation = models.BooleanField(custom=True, db_column='Attended_Family_Orientation__c', verbose_name='Attended Family Orientation', default=models.DEFAULTED_ON_CREATE)
    withdrew_application_detail = models.CharField(custom=True, db_column='Withdrew_Application_Detail__c', max_length=255, verbose_name='Withdrew-Application Detail', help_text='"Dropped in first 2 weeks" means that they showed up for class but decided to drop within the first 2 weeks.', choices=[("Didn't show up for interview", "Didn't show up for interview"), ('Acceptance-offer-rejected', 'Acceptance-offer-rejected'), ('Didn’t show up for class', 'Didn’t show up for class'), ('Dropped in first 2 weeks', 'Dropped in first 2 weeks'), ('Withdrew before interview', 'Withdrew before interview'), ('Class Cancelled', 'Class Cancelled')], blank=True, null=True)
    contact_race = models.CharField(custom=True, db_column='Contact_Race__c', max_length=100, verbose_name='Contact - Race', help_text='DO NOT EDIT - AUTO-POPULATED BY SYSTEM', blank=True, null=True)
    contact_gender = models.CharField(custom=True, db_column='Contact_Gender__c', max_length=30, verbose_name='Contact - Gender', help_text='DO NOT EDIT - AUTO-POPULATED BY SYSTEM', blank=True, null=True)
    parent_contact = models.ForeignKey('Contact', models.DO_NOTHING, db_column='Parent_Contact__c', custom=True, related_name='classenrollment_parentcontact_set', blank=True, null=True)
    attended_interview = models.BooleanField(custom=True, db_column='Attended_Interview__c', verbose_name='Attended Interview', default=models.DEFAULTED_ON_CREATE, help_text='Check if the student attended the default student admissions interview event. Note: Do not check this field if the student attended a makeup interview.')
    attended_makeup_interview = models.BooleanField(custom=True, db_column='Attended_Makeup_Interview__c', verbose_name='Attended Makeup Interview', default=models.DEFAULTED_ON_CREATE, help_text='Check if the student did not attend the default interview date, but attended a makeup session.')
    cultural_affiliation_or_nationality = models.CharField(custom=True, db_column='Cultural_Affiliation_or_Nationality__c', max_length=100, verbose_name='Cultural Affiliation or Nationality', help_text='(optional)', blank=True, null=True)
    sex_at_birth = models.CharField(custom=True, db_column='Sex_at_birth__c', max_length=255, verbose_name='What was your sex at birth?', help_text='(Check one)', choices=[('Female', 'Female'), ('Male', 'Male'), ('Decline to answer', 'Decline to answer')], blank=True, null=True)
    sexual_orientation = models.CharField(custom=True, db_column='Sexual_orientation__c', max_length=255, verbose_name='Sexual orientation or sexual identity', help_text='How do you describe your sexual orientation or sexual identity?', choices=[('Bisexual', 'Bisexual'), ('Gay / Lesbian / Same-Gender Loving', 'Gay / Lesbian / Same-Gender Loving'), ('Questioning / Unsure', 'Questioning / Unsure'), ('Straight / Heterosexual', 'Straight / Heterosexual'), ('Not Listed.', 'Not Listed.'), ('Decline to answer', 'Decline to answer')], blank=True, null=True)
    other_sexual_orientation = models.CharField(custom=True, db_column='Other_sexual_orientation__c', max_length=30, verbose_name='Other sexual orientation', blank=True, null=True)
    household_type = models.CharField(custom=True, db_column='Household_type__c', max_length=255, verbose_name='Which best describes your family?', help_text='Which best describes your family? (Check one)\r\nFamily includes, but is not limited to the following—regardless of actual or perceived sexual orientation, gender identity, or marital status—a single person or a group of persons residing together.', choices=[('Single Female Headed Family', 'Single Female Headed Family'), ('Single Male Headed Family', 'Single Male Headed Family'), ('Dual Headed Family', 'Dual Headed Family')], blank=True, null=True)
    income_certification = models.CharField(custom=True, db_column='Income_Certification__c', max_length=4099, verbose_name='Income Certification', help_text='**current-within 2 months', choices=[('CalWorks', 'CalWorks'), ('Food Stamps', 'Food Stamps'), ('Medi-CAL', 'Medi-CAL'), ('Tax Return (most recent)', 'Tax Return (most recent)'), ('Unemployment (check stub)', 'Unemployment (check stub)'), ('SSI**', 'SSI**'), ('Payroll Stub**', 'Payroll Stub**'), ('Other (i.e. public housing/foster care)**', 'Other (i.e. public housing/foster care)**'), ('Self-certified', 'Self-certified')], blank=True, null=True)
    estimated_income = models.DecimalField(custom=True, db_column='Estimated_income__c', max_digits=18, decimal_places=2, verbose_name='Estimated income', help_text='Total estimated income for next 12 months for all adult members.', blank=True, null=True)
    family_size = models.CharField(custom=True, db_column='Family_size__c', max_length=255, verbose_name='Family size', help_text='Number of persons living in your family (including yourself):', choices=[('1 person', '1 person'), ('2 persons', '2 persons'), ('3 persons', '3 persons'), ('4 persons', '4 persons'), ('5 persons', '5 persons'), ('6 persons', '6 persons'), ('7 persons', '7 persons'), ('8 persons', '8 persons'), ('9+ persons', '9+ persons')], blank=True, null=True)
    current_income_information = models.CharField(custom=True, db_column='Current_Income_Information__c', max_length=255, verbose_name='Current Income Information', choices=[('Extremely Low Income $0 - 27,650 (1 person)', 'Extremely Low Income $0 - 27,650 (1 person)'), ('Low Income $27,651 - 46,100 (1 person)', 'Low Income $27,651 - 46,100 (1 person)'), ('Moderate Income $46,101 - 73,750 (1 person)', 'Moderate Income $46,101 - 73,750 (1 person)'), ('Above Moderate Income $73,751 or greater (1 person)', 'Above Moderate Income $73,751 or greater (1 person)'), ('Extremely Low Income $0 - 31,600 (2 persons)', 'Extremely Low Income $0 - 31,600 (2 persons)'), ('Low Income $31,601 - 52,650 (2 persons)', 'Low Income $31,601 - 52,650 (2 persons)'), ('Moderate Income $52,651 - 84,300 (2 persons)', 'Moderate Income $52,651 - 84,300 (2 persons)'), ('Above Moderate Income $84,301 or greater (2 persons)', 'Above Moderate Income $84,301 or greater (2 persons)'), ('Extremely Low Income $0 - 35,550 (3 persons)', 'Extremely Low Income $0 - 35,550 (3 persons)'), ('Low Income $35,551 - 59,250 (3 persons)', 'Low Income $35,551 - 59,250 (3 persons)'), ('Moderate Income $59,251 - 94,850 (3 persons)', 'Moderate Income $59,251 - 94,850 (3 persons)'), ('Above Moderate Income $94,851 or greater (3 persons)', 'Above Moderate Income $94,851 or greater (3 persons)'), ('Extremely Low Income $0 - 39,500 (4 persons)', 'Extremely Low Income $0 - 39,500 (4 persons)'), ('Low Income $39,501 - 65,800 (4 persons)', 'Low Income $39,501 - 65,800 (4 persons)'), ('Moderate Income $65,801 - 105,350 (4 persons)', 'Moderate Income $65,801 - 105,350 (4 persons)'), ('Above Moderate Income $105,351 or greater (4 persons)', 'Above Moderate Income $105,351 or greater (4 persons)'), ('Extremely Low Income $0 - 42,700 (5 persons)', 'Extremely Low Income $0 - 42,700 (5 persons)'), ('Low Income $42,701 - 71,100 (5 persons)', 'Low Income $42,701 - 71,100 (5 persons)'), ('Moderate Income $71,101 - 113,800 (5 persons)', 'Moderate Income $71,101 - 113,800 (5 persons)'), ('Above Moderate Income $113,801 or greater (5 persons)', 'Above Moderate Income $113,801 or greater (5 persons)'), ('Extremely Low Income $0 - 45,850 (6 persons)', 'Extremely Low Income $0 - 45,850 (6 persons)'), ('Low Income $45,851 - 76,350 (6 persons)', 'Low Income $45,851 - 76,350 (6 persons)'), ('Moderate Income $76,351 - 122,250 (6 persons)', 'Moderate Income $76,351 - 122,250 (6 persons)'), ('Above Moderate Income $122,251 or greater (6 persons)', 'Above Moderate Income $122,251 or greater (6 persons)'), ('Extremely Low Income $0 - 49,000 (7 persons)', 'Extremely Low Income $0 - 49,000 (7 persons)'), ('Low Income $49,001 - 81,600 (7 persons)', 'Low Income $49,001 - 81,600 (7 persons)'), ('Moderate Income $81,601 - 130,650 (7 persons)', 'Moderate Income $81,601 - 130,650 (7 persons)'), ('Above Moderate Income $130,651 or greater (7 persons)', 'Above Moderate Income $130,651 or greater (7 persons)'), ('Extremely Low Income $0 - 52,150 (8 persons)', 'Extremely Low Income $0 - 52,150 (8 persons)'), ('Low Income $52,151 - 86,900 (8 persons)', 'Low Income $52,151 - 86,900 (8 persons)'), ('Moderate Income $86,901 - 139,100 (8 persons)', 'Moderate Income $86,901 - 139,100 (8 persons)'), ('Above Moderate Income $139,101 or greater (8 persons)', 'Above Moderate Income $139,101 or greater (8 persons)')], blank=True, null=True)
    if_self_certified_please_explain = models.TextField(custom=True, db_column='If_self_certified_please_explain__c', verbose_name='If self-certified, please explain:', blank=True, null=True)
    contact_ethnicity = models.CharField(custom=True, db_column='Contact_Ethnicity__c', max_length=100, verbose_name='Contact - Ethnicity', help_text='DO NOT EDIT - AUTO-POPULATED BY SYSTEM', blank=True, null=True)
    notes = models.TextField(custom=True, blank=True, null=True)
    interview_date = models.DateTimeField(custom=True, db_column='Interview_Date__c', verbose_name='Interview Date', help_text="This is the interview date and time that the student signed up for. Empty means that the student did not sign up for an interview. Having an interview date does not mean that the student showed up for the interview, only that they RSVP'ed.", blank=True, null=True)
    returner = models.BooleanField(custom=True, verbose_name='Returner?', sf_read_only=models.READ_ONLY)
    temp_returner = models.BooleanField(custom=True, db_column='Temp_Returner__c', verbose_name='Returner? (temp)', default=models.DEFAULTED_ON_CREATE, help_text='This is a temporary field that determines if a student is a returner based on their response to this question on the application. Once we complete migrating all of our past data into Salesforce, this field will be deleted.')
    origin_school = models.CharField(custom=True, db_column='Origin_School__c', max_length=1300, verbose_name='School attended by this student', sf_read_only=models.READ_ONLY, blank=True, null=True)
    parent_phone = models.CharField(custom=True, db_column='Parent_Phone__c', max_length=1300, verbose_name='Parent Phone', sf_read_only=models.READ_ONLY, blank=True, null=True)
    parent_email = models.CharField(custom=True, db_column='Parent_Email__c', max_length=1300, verbose_name='Parent Email', sf_read_only=models.READ_ONLY, blank=True, null=True)

    class Meta(models.Model.Meta):
        db_table = 'Class_Enrollment__c'
        verbose_name = 'Class Enrollment'
        verbose_name_plural = 'Class Enrollments'
        # keyPrefix = 'a0i'

