from clients.errors_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema, ValidationErrorSchema
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    ExerciseSchema, GetExercisesResponseSchema, UpdateExerciseResponseSchema, UpdateExerciseRequestSchema, \
    GetExerciseResponseSchema
from tools.assertions.errors import assert_internal_error_response, assert_validation_error, \
    assert_validation_error_response
from tools.assertions.methods.assert_equal import assert_equal
from tools.assertions.methods.assert_is_true import assert_is_true
from tools.assertions.methods.assert_length import assert_length


def assert_create_exercise(request: CreateExerciseRequestSchema, response: CreateExerciseResponseSchema):
    assert_is_true(response.exercise.id, "id")
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


def assert_get_exercise(request: ExerciseSchema, response: ExerciseSchema):
    assert_equal(response.id, request.id, "id")
    assert_equal(response.title, request.title, "title")
    assert_equal(response.course_id, request.course_id, "course_id")
    assert_equal(response.max_score, request.max_score, "max_score")
    assert_equal(response.min_score, request.min_score, "min_score")
    assert_equal(response.order_index, request.order_index, "order_index")
    assert_equal(response.description, request.description, "description")
    assert_equal(response.estimated_time, request.estimated_time, "estimated_time")


def assert_get_exercise_response(request: ExerciseSchema, response: GetExerciseResponseSchema):
    assert_get_exercise(request, response.exercise)

def assert_get_exercise_with_incorrect_data_response(actual: ValidationErrorResponseSchema):
    expected=ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",
                input="incorrect-exercise-id",
                context={
                    "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"},
                message="Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1",
                location=["path", "exercise_id"]
            )
        ]
    )
    assert_validation_error_response(actual, expected)
def assert_get_exercises_with_incorrect_data_response(actual: ValidationErrorResponseSchema):
    expected=ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",
                input="incorrect-course-id",
                context={
                    "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"},
                message="Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1",
                location=["query", "courseId"]
            )
        ]
    )
    assert_validation_error_response(actual, expected)
def assert_get_exercises_response(get_exercises_response: GetExercisesResponseSchema,
                                  create_exercises_response: list[CreateExerciseResponseSchema]):
    assert_length(get_exercises_response.exercises, create_exercises_response, "exercises")
    for index, create_exercise_response in enumerate(create_exercises_response):
        assert_get_exercise(get_exercises_response.exercises[index], create_exercise_response.exercise)


def assert_update_exercise_with_incorrect_data_response(actual: ValidationErrorResponseSchema, incorrect_value, location):
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",
                input=incorrect_value,
                context={"min_length": 1},
                message="String should have at least 1 character",
                location=["body", location]
            )
        ]
    )
    assert_validation_error_response(actual, expected)

def assert_update_exercise_response(request: UpdateExerciseRequestSchema, response: UpdateExerciseResponseSchema):
    if request.title is not None:
        assert_equal(response.exercise.title, request.title, "title")
    if request.max_score is not None:
        assert_equal(response.exercise.max_score, request.max_score, "max_score")
    if request.min_score is not None:
        assert_equal(response.exercise.min_score, request.min_score, "min_score")
    if request.order_index is not None:
        assert_equal(response.exercise.order_index, request.order_index, "order_index")
    if request.description is not None:
        assert_equal(response.exercise.description, request.description, "description")
    if request.estimated_time is not None:
        assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


def assert_exercise_not_found_response(actual: InternalErrorResponseSchema):
    expected = InternalErrorResponseSchema(details="Exercise not found")
    assert_internal_error_response(actual, expected)


def assert_create_exercise_with_incorrect_data_response(actual: ValidationErrorResponseSchema, incorrect_value,
                                                        location, type_text, context, message):
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type=type_text,
                input=incorrect_value,
                context=context,
                message=message,
                location=["body", location]
            )
        ]
    )
    assert_validation_error_response(actual, expected)
