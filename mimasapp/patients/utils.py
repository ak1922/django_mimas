import logging
from decimal import Decimal
from django.utils import timezone
from django.db import transaction

from dentists.models import DentistReport, ArchivedDentistReport
from patients.models import (
    PatientLab,
    PatientBill,
    PatientVisit,
    PatientReferral,
    PatientTreatment,
    ArchivedPatientLab,
    ArchivedPatientBill,
    ArchivedPatientVisit,
    ArchivedPatientReferral,
    ArchivedPatientTreatment,
    ArchivedPatientAppointment
)


logger = logging.getLogger(__name__)


# Archive patient visit
def perform_archiving(vis_id):

    now = timezone.now()

    try:
        visit_to_archive = PatientVisit.objects.get(id=vis_id)
        if hasattr(visit_to_archive, 'archivedpatientvisit'):
            return

        bills_to_archive = PatientBill.objects.filter(visit=visit_to_archive)

        closed_labs = PatientLab.laboratories.closed_labs().filter(visit=visit_to_archive)
        closed_reports = DentistReport.reports.closed_reports().filter(visit=visit_to_archive)
        closed_referrals = PatientReferral.referrals.closed_referrals().filter(visit=visit_to_archive)
        closed_treatments = PatientTreatment.objects.closed_treatments().filter(visit=visit_to_archive)

        services_to_archive = list(visit_to_archive.services.all())
        total_price = sum(service.price for service in services_to_archive if service.price is not None)

        with transaction.atomic():
            original_appointment = visit_to_archive.appointment

            # Archive patient appointment
            archived_appointment = ArchivedPatientAppointment.objects.create(
                id=original_appointment.id,
                patient=original_appointment.patient,
                dentist=original_appointment.dentist,
                branch=original_appointment.branch,
                insurance=original_appointment.insurance,
                appointment_title=original_appointment,
                appointment_date=original_appointment.appointment_date,
                appointment_time=original_appointment.appointment_time,
                confirmed=True,
                reason=original_appointment.reason,
                archived=now,
                updated=original_appointment.updated,
                updated_by=original_appointment.updated_by
            )
            logger.info('ArchivedPatientAppointment object created.')

            # Archive patient visit
            archived_visit, created = ArchivedPatientVisit.objects.get_or_create(
                id=visit_to_archive.id,
                defaults={
                    'patient': visit_to_archive.patient,
                    'dentist': visit_to_archive.dentist,
                    'branch': visit_to_archive.branch,
                    'insurance': visit_to_archive.insurance,
                    'appointment': archived_appointment,
                    'visit_title': visit_to_archive.visit_title,
                    'visit_date': visit_to_archive.visit_date,
                    'visit_time': visit_to_archive.visit_time,
                    'visit_status': visit_to_archive.visit_status,
                    'archived': now,
                    'updated': visit_to_archive.updated,
                    'updated_by': visit_to_archive.updated_by,
                    'total_price_aggregated': Decimal(str(total_price))
                }
            )
            logger.info('ArchivedPatientVisit object created.')
            archived_visit.departments.set(visit_to_archive.departments.all())
            archived_visit.services.set(visit_to_archive.services.all())
            archived_visit.visit_options.set(visit_to_archive.visit_options.all())

            # Archive patient labs
            for lab in closed_labs:
                ArchivedPatientLab.objects.create(
                    patient=lab.patient,
                    dentist=lab.dentist,
                    branch=lab.branch,
                    insurance=lab.insurance,
                    appointment=archived_appointment,
                    visit=archived_visit,
                    archived_title=lab.lab_title,
                    laboratory_name=lab.laboratory_name,
                    laboratory_address=lab.laboratory_address,
                    laboratory_phone=lab.laboratory_phone,
                    due_date=lab.due_date,
                    instructions=lab.instructions,
                    closed=True,
                    archived=now,
                    updated=visit_to_archive.updated,
                    updated_by=visit_to_archive.updated_by
                )
                lab.delete()
                logger.info('ArchivedPatientLab object created, original deleted.')

            # Archive patient referrals
            for referral in closed_referrals:
                ArchivedPatientReferral.objects.create(
                    patient=referral.patient,
                    dentist=referral.dentist,
                    branch=referral.branch,
                    insurance=referral.insurance,
                    appointment=archived_appointment,
                    visit=archived_visit,
                    referral_title=referral.referral_title,
                    referral_date=referral.referral_date,
                    refer_phone=referral.referral_phone,
                    reason=referral.reason,
                    extra_details=referral.extra_details,
                    closed=True,
                    archived=now,
                    updated=visit_to_archive.updated,
                    updated_by=visit_to_archive.updated_by
                )
                referral.delete()
                logger.info('ArchivedPatientReferral object created, original deleted.')

            # Archive patient treatments
            for treatment in closed_treatments:
                ArchivedPatientTreatment.objects.create(
                    patient=treatment.patient,
                    dentist=treatment.dentist,
                    branch=treatment.branch,
                    insurance=treatment.insurance,
                    appointment=archived_appointment,
                    visit=archived_visit,
                    treatment_title=treatment.treatment_title,
                    teeth_number=treatment.teeth_number,
                    medication=treatment.medication,
                    notes=treatment.notes,
                    closed=True,
                    archived=now,
                    updated=visit_to_archive.updated,
                    updated_by=visit_to_archive.updated_by
                )
                treatment.delete()
                logger.info('ArchivedPatientTreatment object created, original treatment deleted.')

            # Archive dentist report
            for report in closed_reports:
                ArchivedDentistReport.objects.create(
                    patient=report.patient,
                    dentist=report.dentist,
                    branch=report.branch,
                    insurance=report.insurance,
                    appointment=archived_appointment,
                    visit=archived_visit,
                    archived_title=report.report_title,
                    history=report.history,
                    clinical_finding=report.clinical_finding,
                    diagnosis=report.diagnosis,
                    general_comments=report.general_comments,
                    closed=True,
                    archived=now,
                    updated=visit_to_archive.updated,
                    updated_by=visit_to_archive.updated_by
                )
                report.delete()
                logger.info('ArchivedDentistReport object created, original report deleted.')

            # Archive visit bill
            for bill in bills_to_archive:
                ArchivedPatientBill.objects.create(
                    patient=bill.patient,
                    appointment=archived_appointment,
                    visit=archived_visit,
                    bill_title=bill.bill_title,
                    total_charge=str(bill.total_charge),
                    is_paid=bill.is_paid,
                    archived=now,
                    updated=visit_to_archive.updated,
                    updated_by=visit_to_archive.updated_by
                )
                bill.delete()
                logger.info('ArchivedPatientBill object created, original report deleted.')

            PatientLab.objects.filter(visit=visit_to_archive).delete()
            PatientBill.objects.filter(visit=visit_to_archive).delete()
            DentistReport.objects.filter(visit=visit_to_archive).delete()
            PatientReferral.objects.filter(visit=visit_to_archive).delete()
            PatientTreatment.objects.filter(visit=visit_to_archive).delete()

            visit_to_archive.delete()
            original_appointment.delete()

    except PatientVisit.DoesNotExist:
        logger.error(f"PatientVisit with id {vis_id} does not exist.")
    except Exception as e:
        logger.exception("An error occurred during archiving.")
        raise e
