from apiflask import Schema
from apiflask.fields import List, Float, Integer, String, File
from apiflask.validators import OneOf, FileType

mimetypes = {
    'csv': ['text/csv'],
    'excel': [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
    ],
}


class ObservationsIn(Schema):
    stage = List(Float, required=True, description='Stage observations')
    discharge = List(Float, required=True, description='Discharge observations')
    discharge_se = List(Float, required=False, description='Discharge standard error')


class RatingOut(Schema):
    stage = List(Float, description='Stage')
    discharge = List(Float, description='Expected discharge')
    median = List(Float, description='Median discharge')
    gse = List(Float, description='Geometric standard error')


class RRTIn(Schema):
    csv = File(
        required=True,
        validate=FileType(['.csv', '.xlsx', '.xls']),
        description='Excel or CSV file containing field observations exported from RRT',
    )


class RRTOut(Schema):
    csv = File(
        description='CSV file containing a rating table to be imported into RRT',
    )


class FitPowerLawQuery(Schema):
    segments = Integer(
        load_default=1,
        validate=lambda x: x > 0,
        description='Number of segments in the rating curve',
    )
    method = String(
        load_default='advi',
        validate=OneOf(['advi', 'nuts']),
        description='Fit with ADVI (fast) or NUTS (accurate)',
    )
