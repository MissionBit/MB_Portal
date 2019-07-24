from home.decorators import group_required_multiple
from django import forms
from django.shortcuts import render, redirect
from home.models.models import Classroom, Attendance
from home.models.salesforce import ClassOffering
from staff.staff_views_helper import class_offering_meeting_dates
from datetime import datetime
from django.template.defaulttags import register
from django_q.tasks import async_task


@group_required_multiple('staff', 'teacher')
def attendance(request):
    if request.method == "POST":
        store_attendance_data(request)
        async_task("attendance.views.update_course_attendance_statistic", request.POST.get("course_id"))
        return redirect("attendance")
    if request.GET.get("course_id") is not None:
        course_id = request.GET.get("course_id")
        context = get_classroom_attendance(course_id)
        context.update(
            {
                "attendance_statistic": get_course_attendance_statistic(course_id)
            }
        )
    else:
        attendance_averages = compile_attendance_averages_for_all_courses()
        context = {
            "classrooms": Classroom.objects.all(),
            "attendance_averages": attendance_averages,
        }
    return render(request, "attendance.html", context)


@group_required_multiple('staff', 'teacher')
def take_attendance(request):
    context = take_attendance_context(
        request.GET.get("course_id"),
        get_date_from_template_returned_string(request.GET.get("date")),
    )
    return render(request, "attendance.html", context)


def get_classroom_attendance(course_id):
    dates = get_classroom_meeting_dates(course_id)
    classroom_attendance = Attendance.objects.filter(classroom_id=course_id)
    course = Classroom.objects.get(id=course_id).course
    daily_attendance = compile_daily_attendance_for_course(course_id)
    return {
        "classroom_attendance": classroom_attendance,
        "dates": dates,
        "course": course,
        "course_id": course_id,
        "daily_attendance": daily_attendance,
    }


def take_attendance_context(course_id, date):
    course = Classroom.objects.get(id=course_id).course
    attendance_objects = Attendance.objects.filter(classroom_id=course_id, date=date)
    return {
        "course_name": course,
        "course_id": course_id,
        "attendance_objects": attendance_objects,
    }


@group_required_multiple('staff', 'teacher')
def store_attendance_data(request):
    date = get_date_from_template_returned_string(request.POST.get("date"))
    course_id = request.POST.get("course_id")
    attendance_objects = Attendance.objects.filter(classroom_id=course_id, date=date)
    for attendance_object in attendance_objects:
        attendance_object.presence = request.POST.get(str(attendance_object.student))
        attendance_object.save()


def compile_attendance_averages_for_all_courses():
    attendance_averages = {}
    for classroom in Classroom.objects.all():
        stat = get_course_attendance_statistic(classroom.id)
        attendance_averages.update({classroom.course: stat})
    return attendance_averages


def compile_daily_attendance_for_course(course_id):
    daily_attendance_record = {}
    dates = get_classroom_meeting_dates(course_id)
    for date in dates:
        daily_attendance = Attendance.objects.filter(classroom_id=course_id, date=date)
        average = round(get_average_attendance_from_list(daily_attendance) * 100, 2)
        daily_attendance_record.update({date: average})
    return daily_attendance_record


def get_average_attendance_from_list(list):
    return sum(
        attendance_object.presence == "Present" or attendance_object.presence == "Late"
        for attendance_object in list
    ) / len(list) if len(list) > 0 else 0


def get_classroom_meeting_dates(course_id):
    return class_offering_meeting_dates(
        ClassOffering.objects.get(name=Classroom.objects.get(id=course_id).course)
    )


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def get_date_from_template_returned_string(string_date):
    return datetime.strptime(string_date, "%B %d, %Y").date()


def update_course_attendance_statistic(course_id):
    class_attendance = Attendance.objects.filter(classroom_id=course_id, date__range=["2000-01-01", datetime.today().date()])
    average = get_average_attendance_from_list(class_attendance)
    classroom = Classroom.objects.get(id=course_id)
    classroom.attendance_summary = {"attendance_statistic": round(average * 100, 2)}
    classroom.save()


def get_course_attendance_statistic(course_id):
    return Classroom.objects.get(id=course_id).attendance_summary.get("attendance_statistic")
