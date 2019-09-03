from salesforce import models
from home.choices import *


class Account(models.Model):
    is_deleted = models.BooleanField(
        verbose_name="Deleted", sf_read_only=models.READ_ONLY, default=False
    )
    master_record = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        related_name="account_masterrecord_set",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255, verbose_name="Account Name")
    type = models.CharField(
        max_length=40,
        verbose_name="Account Type",
        choices=ACCOUNT_TYPE_CHOICES,
        blank=True,
        null=True,
    )
    parent = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        related_name="account_parent_set",
        blank=True,
        null=True,
    )
    billing_street = models.TextField(blank=True, null=True)
    billing_city = models.CharField(max_length=40, blank=True, null=True)
    billing_state = models.CharField(
        max_length=80, verbose_name="Billing State/Province", blank=True, null=True
    )
    billing_postal_code = models.CharField(
        max_length=20, verbose_name="Billing Zip/Postal Code", blank=True, null=True
    )
    billing_country = models.CharField(max_length=80, blank=True, null=True)
    npe01_systemis_individual = models.BooleanField(
        db_column="npe01__SYSTEMIsIndividual__c",
        custom=True,
        verbose_name="_SYSTEM: IsIndividual",
        default=models.DEFAULTED_ON_CREATE,
        help_text="Indicates whether or not this Account is special for Contacts (Household, One-to-One, Individual) vs a normal Account.",
    )

    class Meta(models.Model.Meta):
        db_table = "Account"
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        # keyPrefix = '001'

    def __str__(self):
        return "%s" % self.name


class Contact(models.Model):
    is_deleted = models.BooleanField(
        verbose_name="Deleted", sf_read_only=models.READ_ONLY, default=False
    )
    master_record = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        related_name="contact_masterrecord_set",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    account = models.ForeignKey(
        Account,
        models.DO_NOTHING,
        related_name="contact_account_set",
        blank=True,
        null=True,
    )  # Master Detail Relationship *
    last_name = models.CharField(max_length=80)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    salutation = models.CharField(
        max_length=40, choices=SALUTATION_CHOICES, blank=True, null=True
    )
    middle_name = models.CharField(max_length=40, blank=True, null=True)
    suffix = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(
        max_length=121, verbose_name="Full Name", sf_read_only=models.READ_ONLY
    )
    mailing_street = models.TextField(blank=True, null=True)
    mailing_city = models.CharField(max_length=40, blank=True, null=True)
    mailing_state = models.CharField(
        max_length=80, verbose_name="Mailing State/Province", blank=True, null=True
    )
    mailing_postal_code = models.CharField(
        max_length=20, verbose_name="Mailing Zip/Postal Code", blank=True, null=True
    )
    mailing_country = models.CharField(max_length=80, blank=True, null=True)
    mailing_state_code = models.CharField(
        max_length=10,
        verbose_name="Mailing State/Province Code",
        choices=STATE_CHOICES,
        blank=True,
        null=True,
    )
    mailing_country_code = models.CharField(
        max_length=10,
        default=models.DEFAULTED_ON_CREATE,
        choices=STATE_CHOICES,
        blank=True,
        null=True,
    )
    mobile_phone = models.CharField(max_length=40, blank=True, null=True)
    home_phone = models.CharField(max_length=40, blank=True, null=True)
    other_phone = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    department = models.CharField(max_length=80, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    owner = models.ForeignKey(
        "User", models.DO_NOTHING, related_name="contact_owner_set", blank=True
    )
    created_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    created_by = models.ForeignKey(
        "User",
        models.DO_NOTHING,
        related_name="contact_createdby_set",
        sf_read_only=models.READ_ONLY,
    )
    last_modified_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    last_modified_by = models.ForeignKey(
        "User",
        models.DO_NOTHING,
        related_name="contact_lastmodifiedby_set",
        sf_read_only=models.READ_ONLY,
    )
    system_modstamp = models.DateTimeField(sf_read_only=models.READ_ONLY)
    last_activity_date = models.DateField(
        verbose_name="Last Activity",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    last_curequest_date = models.DateTimeField(
        db_column="LastCURequestDate",
        verbose_name="Last Stay-in-Touch Request Date",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    last_cuupdate_date = models.DateTimeField(
        db_column="LastCUUpdateDate",
        verbose_name="Last Stay-in-Touch Save Date",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    last_viewed_date = models.DateTimeField(
        sf_read_only=models.READ_ONLY, blank=True, null=True
    )
    last_referenced_date = models.DateTimeField(
        sf_read_only=models.READ_ONLY, blank=True, null=True
    )
    email_bounced_reason = models.CharField(max_length=255, blank=True, null=True)
    email_bounced_date = models.DateTimeField(blank=True, null=True)
    is_email_bounced = models.BooleanField(sf_read_only=models.READ_ONLY, default=False)
    photo_url = models.URLField(
        verbose_name="Photo URL", sf_read_only=models.READ_ONLY, blank=True, null=True
    )
    jigsaw_contact_id = models.CharField(
        max_length=20,
        verbose_name="Jigsaw Contact ID",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    individual = models.ForeignKey(
        "Individual", models.DO_NOTHING, blank=True, null=True
    )
    race = models.CharField(
        custom=True,
        max_length=255,
        verbose_name="Which best describes your race?",
        choices=RACE_CHOICES,
        blank=True,
        null=True,
    )
    gender = models.CharField(
        custom=True, max_length=255, choices=GENDER_CHOICES, blank=True, null=True
    )
    which_best_describes_your_ethnicity = models.CharField(
        custom=True,
        db_column="Which_best_describes_your_ethnicity__c",
        max_length=255,
        verbose_name="Which best describes your ethnicity?",
        choices=ETHNICITY_CHOICES,
        blank=True,
        null=True,
    )
    expected_graduation_year = models.CharField(
        custom=True,
        db_column="Expected_graduation_year__c",
        max_length=4,
        verbose_name="Expected graduation year",
        help_text="Enter the year this contact is expected to graduate.  For example, 2020",
        blank=True,
        null=True,
    )
    current_grade_level = models.CharField(
        custom=True,
        db_column="Current_grade_level__c",
        max_length=1300,
        verbose_name="Current grade level",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    volunteer_area_s_of_interest = models.CharField(
        custom=True,
        db_column="Volunteer_area_s_of_interest__c",
        max_length=4099,
        verbose_name="Volunteer area(s) of interest",
        choices=[("Classroom", "Classroom"), ("Event", "Event"), ("Other", "Other")],
        blank=True,
        null=True,
    )
    enrollments_this_semester_applied = models.DecimalField(
        custom=True,
        db_column="enrollments_this_semester_Applied__c",
        max_digits=2,
        decimal_places=0,
        verbose_name="# enrollments this semester - Applied",
        help_text="DO NOT EDIT - AUTO-POPULATED BY SYSTEM",
        blank=True,
        null=True,
    )
    enrollments_this_semester_waitlisted = models.DecimalField(
        custom=True,
        db_column="enrollments_this_semester_Waitlisted__c",
        max_digits=2,
        decimal_places=0,
        verbose_name="# enrollments this semester - Waitlisted",
        help_text="DO NOT EDIT - AUTO-POPULATED BY SYSTEM",
        blank=True,
        null=True,
    )
    enrollments_this_semester_rejected = models.DecimalField(
        custom=True,
        db_column="enrollments_this_semester_Rejected__c",
        max_digits=2,
        decimal_places=0,
        verbose_name="# enrollments this semester - Rejected",
        help_text="DO NOT EDIT - AUTO-POPULATED BY SYSTEM",
        blank=True,
        null=True,
    )
    enrollments_this_semester_drop_out = models.DecimalField(
        custom=True,
        db_column="enrollments_this_semester_Drop_out__c",
        max_digits=2,
        decimal_places=0,
        verbose_name="# enrollments this semester - Drop out",
        help_text="DO NOT EDIT - AUTO-POPULATED BY SYSTEM",
        blank=True,
        null=True,
    )
    race_other = models.CharField(
        custom=True,
        db_column="Race_Other__c",
        max_length=100,
        verbose_name="Which best describes your race? (Other)",
        blank=True,
        null=True,
    )
    gender_other = models.CharField(
        custom=True,
        db_column="Gender_Other__c",
        max_length=50,
        verbose_name="Gender (Other)",
        blank=True,
        null=True,
    )
    parent_guardian_first_name = models.CharField(
        custom=True,
        db_column="Parent_Guardian_first_name__c",
        max_length=100,
        verbose_name="Parent/Guardian first name",
        blank=True,
        null=True,
    )
    parent_guardian_last_name = models.CharField(
        custom=True,
        db_column="Parent_Guardian_last_name__c",
        max_length=100,
        verbose_name="Parent/Guardian last name",
        blank=True,
        null=True,
    )
    parent_guardian_phone = models.CharField(
        custom=True,
        db_column="Parent_Guardian_phone__c",
        max_length=40,
        verbose_name="Parent/Guardian phone",
        blank=True,
        null=True,
    )
    parent_guardian_email = models.EmailField(
        custom=True,
        db_column="Parent_Guardian_email__c",
        verbose_name="Parent/Guardian email",
        blank=True,
        null=True,
    )
    dm_current_grade = models.CharField(
        custom=True,
        db_column="DM_Current_grade__c",
        max_length=255,
        verbose_name="DM - Current grade",
        help_text="Need this for data migration to calculate Expected Graduation Year?  If not, delete this field.",
        choices=CURRENT_GRADE_CHOICES,
        blank=True,
        null=True,
    )
    client_id = models.CharField(
        custom=True,
        db_column="Client_ID__c",
        max_length=14,
        verbose_name="Client ID",
        help_text='3 first letters of first name, 3 first letters of last name, and birthdate "AAABBB00000000" (Only used for students and parents). This field is auto-populated by FormAssembly.',
        blank=True,
        null=True,
    )
    npsp_primary_affiliation = models.ForeignKey(
        Account,
        models.DO_NOTHING,
        db_column="npsp__Primary_Affiliation__c",
        custom=True,
        related_name="contact_npspprimaryaffiliation_set",
        blank=True,
        null=True,
    )

    class Meta(models.Model.Meta):
        db_table = "Contact"
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        # keyPrefix = '003'

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class User(models.Model):
    username = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    middle_name = models.CharField(max_length=40, blank=True, null=True)
    suffix = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(
        max_length=121, verbose_name="Full Name", sf_read_only=models.READ_ONLY
    )
    company_name = models.CharField(max_length=80, blank=True, null=True)
    division = models.CharField(max_length=80, blank=True, null=True)
    department = models.CharField(max_length=80, blank=True, null=True)
    title = models.CharField(max_length=80, blank=True, null=True)
    street = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    state = models.CharField(
        max_length=80, verbose_name="State/Province", blank=True, null=True
    )
    postal_code = models.CharField(
        max_length=20, verbose_name="Zip/Postal Code", blank=True, null=True
    )
    country = models.CharField(max_length=80, blank=True, null=True)
    is_active = models.BooleanField(
        verbose_name="Active", default=models.DEFAULTED_ON_CREATE
    )

    class Meta(models.Model.Meta):
        db_table = "User"
        verbose_name = "User"
        verbose_name_plural = "Users"
        # keyPrefix = '003'

    def __str__(self):
        if self.is_active:
            active = "Active"
        else:
            active = "Inactive"
        return "%s %s -- %s" % (self.first_name, self.last_name, active)


class Individual(models.Model):
    owner = models.ForeignKey(
        "User", models.DO_NOTHING, related_name="individual_owner_set"
    )  # Master Detail Relationship *
    is_deleted = models.BooleanField(
        verbose_name="Deleted", sf_read_only=models.READ_ONLY, default=False
    )
    last_name = models.CharField(max_length=80)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    salutation = models.CharField(
        max_length=40, choices=SALUTATION_CHOICES, blank=True, null=True
    )
    middle_name = models.CharField(max_length=40, blank=True, null=True)
    suffix = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=121, sf_read_only=models.READ_ONLY)

    class Meta(models.Model.Meta):
        db_table = "Individual"
        verbose_name = "Individual"
        verbose_name_plural = "Individuals"
        # keyPrefix = '003'


class ClassOffering(models.Model):
    # owner = models.ForeignKey('Group', models.DO_NOTHING)  # Reference to tables [Group, User]
    is_deleted = models.BooleanField(
        verbose_name="Deleted", sf_read_only=models.READ_ONLY, default=False
    )
    name = models.CharField(
        max_length=80,
        verbose_name="Class Offering Name",
        default=models.DEFAULTED_ON_CREATE,
        blank=True,
        null=True,
    )
    mbportal_id = models.DecimalField(
        custom=True,
        db_column="MBPortal_id__c",
        unique=True,
        max_digits=8,
        decimal_places=0,
        verbose_name="MBPortal_id",
        help_text="This will be automatically set by the Mission Bit Portal, and should not be altered.",
        blank=True,
        null=True,
    )
    created_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    created_by = models.ForeignKey(
        "User",
        models.DO_NOTHING,
        related_name="classoffering_createdby_set",
        sf_read_only=models.READ_ONLY,
    )
    last_modified_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    last_modified_by = models.ForeignKey(
        "User",
        models.DO_NOTHING,
        related_name="classoffering_lastmodifiedby_set",
        sf_read_only=models.READ_ONLY,
    )
    system_modstamp = models.DateTimeField(sf_read_only=models.READ_ONLY)
    last_viewed_date = models.DateTimeField(
        sf_read_only=models.READ_ONLY, blank=True, null=True
    )
    last_referenced_date = models.DateTimeField(
        sf_read_only=models.READ_ONLY, blank=True, null=True
    )
    start_date = models.DateField(
        custom=True,
        db_column="Start_Date__c",
        verbose_name="Start Date",
        blank=True,
        null=True,
    )
    end_date = models.DateField(
        custom=True,
        db_column="End_Date__c",
        verbose_name="End Date",
        blank=True,
        null=True,
    )
    description = models.TextField(custom=True, blank=True, null=True)
    location = models.ForeignKey(
        Account, models.DO_NOTHING, custom=True, blank=True, null=True
    )
    course = models.CharField(
        custom=True, max_length=255, choices=COURSE_CHOICES, blank=True, null=True
    )
    instructor = models.ForeignKey(
        "Contact", models.DO_NOTHING, custom=True, blank=True, null=True
    )
    academic_semester = models.CharField(
        custom=True,
        db_column="Academic_semester__c",
        max_length=1300,
        verbose_name="Academic semester",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    meeting_days = models.CharField(
        custom=True,
        db_column="Meeting_Days__c",
        max_length=255,
        verbose_name="Meeting Days",
        choices=MEETING_DAYS_CHOICES,
        blank=True,
        null=True,
    )
    count_total_female_students = models.DecimalField(
        custom=True,
        db_column="Count_total_female_students__c",
        max_digits=18,
        decimal_places=0,
        verbose_name="Count - Total Female Students",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    count_total_latino_african_american = models.DecimalField(
        custom=True,
        db_column="Count_total_latino_african_american__c",
        max_digits=18,
        decimal_places=0,
        verbose_name="Count - Total African American",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    count_total_latino_students = models.DecimalField(
        custom=True,
        db_column="Count_Total_Latino_Students__c",
        max_digits=18,
        decimal_places=0,
        verbose_name="Count - Total Latino Students",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    female = models.DecimalField(
        custom=True,
        max_digits=18,
        decimal_places=1,
        verbose_name="% Female",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    latino_african_american = models.DecimalField(
        custom=True,
        db_column="Latino_African_American__c",
        max_digits=18,
        decimal_places=1,
        verbose_name="% Latino/African American",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    current_academic_semester = models.CharField(
        custom=True,
        db_column="Current_academic_semester__c",
        max_length=1300,
        verbose_name="Current academic semester",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    in_current_semester = models.BooleanField(
        custom=True,
        db_column="In_current_semester__c",
        verbose_name="In current semester?",
        sf_read_only=models.READ_ONLY,
    )

    class Meta(models.Model.Meta):
        db_table = "Class_Offering__c"
        verbose_name = "Class Offering"
        verbose_name_plural = "Class Offerings"
        # keyPrefix = 'a0h'

    def __str__(self):
        return "%s" % self.name


class ClassEnrollment(models.Model):
    is_deleted = models.BooleanField(
        verbose_name="Deleted", sf_read_only=models.READ_ONLY, default=False
    )
    name = models.CharField(
        max_length=80, verbose_name="Class Enrollment #", sf_read_only=models.READ_ONLY
    )
    created_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    created_by = models.ForeignKey(
        "User",
        models.DO_NOTHING,
        related_name="classenrollment_createdby_set",
        sf_read_only=models.READ_ONLY,
    )
    last_modified_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    last_modified_by = models.ForeignKey(
        "User",
        models.DO_NOTHING,
        related_name="classenrollment_lastmodifiedby_set",
        sf_read_only=models.READ_ONLY,
    )
    system_modstamp = models.DateTimeField(sf_read_only=models.READ_ONLY)
    last_activity_date = models.DateField(
        sf_read_only=models.READ_ONLY, blank=True, null=True
    )
    last_viewed_date = models.DateTimeField(
        sf_read_only=models.READ_ONLY, blank=True, null=True
    )
    last_referenced_date = models.DateTimeField(
        sf_read_only=models.READ_ONLY, blank=True, null=True
    )
    contact = models.ForeignKey(
        "Contact",
        models.DO_NOTHING,
        custom=True,
        related_name="classenrollment_contact_set",
    )  # Master Detail Relationship 0
    role = models.CharField(
        custom=True,
        max_length=255,
        choices=[("Student", "Student"), ("TA", "TA"), ("Volunteer", "Volunteer")],
        blank=True,
        null=True,
    )
    class_offering = models.ForeignKey(
        "ClassOffering", models.DO_NOTHING, db_column="Class_Offering__c", custom=True
    )  # Master Detail Relationship 1
    status = models.CharField(
        custom=True, max_length=255, choices=STATUS_CHOICES, blank=True, null=True
    )
    in_current_semester = models.BooleanField(
        custom=True,
        db_column="In_current_semester__c",
        verbose_name="In current semester?",
        sf_read_only=models.READ_ONLY,
    )
    attended_family_orientation = models.BooleanField(
        custom=True,
        db_column="Attended_Family_Orientation__c",
        verbose_name="Attended Family Orientation",
        default=models.DEFAULTED_ON_CREATE,
    )
    withdrew_application_detail = models.CharField(
        custom=True,
        db_column="Withdrew_Application_Detail__c",
        max_length=255,
        verbose_name="Withdrew-Application Detail",
        help_text='"Dropped in first 2 weeks" means that they showed up for class but decided to drop within the first 2 weeks.',
        choices=APP_WD_CHOICES,
        blank=True,
        null=True,
    )
    contact_race = models.CharField(
        custom=True,
        db_column="Contact_Race__c",
        max_length=100,
        verbose_name="Contact - Race",
        help_text="DO NOT EDIT - AUTO-POPULATED BY SYSTEM",
        blank=True,
        null=True,
    )
    contact_gender = models.CharField(
        custom=True,
        db_column="Contact_Gender__c",
        max_length=30,
        verbose_name="Contact - Gender",
        help_text="DO NOT EDIT - AUTO-POPULATED BY SYSTEM",
        blank=True,
        null=True,
    )
    parent_contact = models.ForeignKey(
        "Contact",
        models.DO_NOTHING,
        db_column="Parent_Contact__c",
        custom=True,
        related_name="classenrollment_parentcontact_set",
        blank=True,
        null=True,
    )
    attended_interview = models.BooleanField(
        custom=True,
        db_column="Attended_Interview__c",
        verbose_name="Attended Interview",
        default=models.DEFAULTED_ON_CREATE,
        help_text="Check if the student attended the default student admissions interview event. Note: Do not check this field if the student attended a makeup interview.",
    )
    attended_makeup_interview = models.BooleanField(
        custom=True,
        db_column="Attended_Makeup_Interview__c",
        verbose_name="Attended Makeup Interview",
        default=models.DEFAULTED_ON_CREATE,
        help_text="Check if the student did not attend the default interview date, but attended a makeup session.",
    )
    cultural_affiliation_or_nationality = models.CharField(
        custom=True,
        db_column="Cultural_Affiliation_or_Nationality__c",
        max_length=100,
        verbose_name="Cultural Affiliation or Nationality",
        help_text="(optional)",
        blank=True,
        null=True,
    )
    sex_at_birth = models.CharField(
        custom=True,
        db_column="Sex_at_birth__c",
        max_length=255,
        verbose_name="What was your sex at birth?",
        help_text="(Check one)",
        choices=SEX_AT_BIRTH_CHOICES,
        blank=True,
        null=True,
    )
    sexual_orientation = models.CharField(
        custom=True,
        db_column="Sexual_orientation__c",
        max_length=255,
        verbose_name="Sexual orientation or sexual identity",
        help_text="How do you describe your sexual orientation or sexual identity?",
        choices=SEXUAL_ORIENTATION_CHOICES,
        blank=True,
        null=True,
    )
    other_sexual_orientation = models.CharField(
        custom=True,
        db_column="Other_sexual_orientation__c",
        max_length=30,
        verbose_name="Other sexual orientation",
        blank=True,
        null=True,
    )
    household_type = models.CharField(
        custom=True,
        db_column="Household_type__c",
        max_length=255,
        verbose_name="Which best describes your family?",
        help_text="Which best describes your family? (Check one)\r\nFamily includes, but is not limited to the following—regardless of actual or perceived sexual orientation, gender identity, or marital status—a single person or a group of persons residing together.",
        choices=HOUSEHOLD_TYPE_CHOICES,
        blank=True,
        null=True,
    )
    income_certification = models.CharField(
        custom=True,
        db_column="Income_Certification__c",
        max_length=4099,
        verbose_name="Income Certification",
        help_text="**current-within 2 months",
        choices=INCOME_CERT_CHOICES,
        blank=True,
        null=True,
    )
    estimated_income = models.DecimalField(
        custom=True,
        db_column="Estimated_income__c",
        max_digits=18,
        decimal_places=2,
        verbose_name="Estimated income",
        help_text="Total estimated income for next 12 months for all adult members.",
        blank=True,
        null=True,
    )
    family_size = models.CharField(
        custom=True,
        db_column="Family_size__c",
        max_length=255,
        verbose_name="Family size",
        help_text="Number of persons living in your family (including yourself):",
        choices=FAMILY_SIZE_CHOICES,
        blank=True,
        null=True,
    )
    current_income_information = models.CharField(
        custom=True,
        db_column="Current_Income_Information__c",
        max_length=255,
        verbose_name="Current Income Information",
        choices=INCOME_LEVEL_CHOICES,
        blank=True,
        null=True,
    )
    if_self_certified_please_explain = models.TextField(
        custom=True,
        db_column="If_self_certified_please_explain__c",
        verbose_name="If self-certified, please explain:",
        blank=True,
        null=True,
    )
    contact_ethnicity = models.CharField(
        custom=True,
        db_column="Contact_Ethnicity__c",
        max_length=100,
        verbose_name="Contact - Ethnicity",
        help_text="DO NOT EDIT - AUTO-POPULATED BY SYSTEM",
        blank=True,
        null=True,
    )
    notes = models.TextField(custom=True, blank=True, null=True)
    interview_date = models.DateTimeField(
        custom=True,
        db_column="Interview_Date__c",
        verbose_name="Interview Date",
        help_text="This is the interview date and time that the student signed up for. Empty means that the student did not sign up for an interview. Having an interview date does not mean that the student showed up for the interview, only that they RSVP'ed.",
        blank=True,
        null=True,
    )
    returner = models.BooleanField(
        custom=True, verbose_name="Returner?", sf_read_only=models.READ_ONLY
    )
    temp_returner = models.BooleanField(
        custom=True,
        db_column="Temp_Returner__c",
        verbose_name="Returner? (temp)",
        default=models.DEFAULTED_ON_CREATE,
        help_text="This is a temporary field that determines if a student is a returner based on their response to this question on the application. Once we complete migrating all of our past data into Salesforce, this field will be deleted.",
    )
    origin_school = models.CharField(
        custom=True,
        db_column="Origin_School__c",
        max_length=1300,
        verbose_name="School attended by this student",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    parent_phone = models.CharField(
        custom=True,
        db_column="Parent_Phone__c",
        max_length=1300,
        verbose_name="Parent Phone",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    parent_email = models.CharField(
        custom=True,
        db_column="Parent_Email__c",
        max_length=1300,
        verbose_name="Parent Email",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )

    class Meta(models.Model.Meta):
        db_table = "Class_Enrollment__c"
        verbose_name = "Class Enrollment"
        verbose_name_plural = "Class Enrollments"
        # keyPrefix = 'a0i'


class ClassMeeting(models.Model):
    is_deleted = models.BooleanField(
        verbose_name="Deleted", sf_read_only=models.READ_ONLY, default=False
    )
    name = models.CharField(
        max_length=80,
        verbose_name="Class Meeting Name",
        default=models.DEFAULTED_ON_CREATE,
        blank=True,
        null=True,
    )
    created_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    created_by = models.ForeignKey(
        "User",
        models.DO_NOTHING,
        related_name="classmeeting_createdby_set",
        sf_read_only=models.READ_ONLY,
    )
    last_modified_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    last_modified_by = models.ForeignKey(
        "User",
        models.DO_NOTHING,
        related_name="classmeeting_lastmodifiedby_set",
        sf_read_only=models.READ_ONLY,
    )
    system_modstamp = models.DateTimeField(sf_read_only=models.READ_ONLY)
    date = models.DateField(custom=True, blank=True, null=True)
    class_offering = models.ForeignKey(
        "ClassOffering", models.DO_NOTHING, db_column="Class_Offering__c", custom=True
    )  # Master Detail Relationship 0
    start_time = models.TimeField(
        custom=True,
        db_column="Start_Time__c",
        verbose_name="Start Time",
        blank=True,
        null=True,
    )
    end_time = models.TimeField(
        custom=True,
        db_column="End_Time__c",
        verbose_name="End Time",
        blank=True,
        null=True,
    )
    duration_hours = models.DecimalField(
        custom=True,
        db_column="Duration_hours__c",
        max_digits=2,
        decimal_places=0,
        verbose_name="Duration (hours)",
        blank=True,
        null=True,
    )

    class Meta(models.Model.Meta):
        db_table = "Class_Meeting__c"
        verbose_name = "Class Meeting"
        verbose_name_plural = "Class Meetings"


class ClassAttendance(models.Model):
    is_deleted = models.BooleanField(
        verbose_name="Deleted", sf_read_only=models.READ_ONLY, default=False
    )
    name = models.CharField(
        max_length=80, verbose_name="Class Attendance #", sf_read_only=models.READ_ONLY
    )
    created_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    created_by = models.ForeignKey(
        "User",
        models.DO_NOTHING,
        related_name="classattendance_createdby_set",
        sf_read_only=models.READ_ONLY,
    )
    last_modified_date = models.DateTimeField(sf_read_only=models.READ_ONLY)
    last_modified_by = models.ForeignKey(
        "User",
        models.DO_NOTHING,
        related_name="classattendance_lastmodifiedby_set",
        sf_read_only=models.READ_ONLY,
    )
    system_modstamp = models.DateTimeField(sf_read_only=models.READ_ONLY)
    contact = models.ForeignKey(
        "Contact", models.DO_NOTHING, custom=True, sf_read_only=models.NOT_UPDATEABLE
    )  # Master Detail Relationship 0
    status = models.CharField(
        custom=True,
        max_length=255,
        choices=[
            ("Present", "Present"),
            ("Late", "Late"),
            ("Excused", "Excused"),
            ("Absent", "Absent"),
            ("Signed-up", "Signed-up"),
        ],
        blank=True,
        null=True,
    )
    class_meeting = models.ForeignKey(
        "ClassMeeting",
        models.DO_NOTHING,
        db_column="Class_Meeting__c",
        custom=True,
        sf_read_only=models.NOT_UPDATEABLE,
    )  # Master Detail Relationship 1
    class_meeting_date = models.DateField(
        custom=True,
        db_column="Class_Meeting_Date__c",
        verbose_name="Class Meeting Date",
        sf_read_only=models.READ_ONLY,
        blank=True,
        null=True,
    )
    assessment_score = models.DecimalField(
        custom=True,
        db_column="Assessment_Score__c",
        max_digits=1,
        decimal_places=0,
        verbose_name="Assessment Score",
        blank=True,
        null=True,
    )
    teacher_s_notes = models.TextField(
        custom=True,
        db_column="Teacher_s_Notes__c",
        verbose_name="Teacher's Notes",
        blank=True,
        null=True,
    )

    class Meta(models.Model.Meta):
        db_table = "Class_Attendance__c"
        verbose_name = "Class Attendance"
        verbose_name_plural = "Class Attendance"
        # keyPrefix = 'a0k'
