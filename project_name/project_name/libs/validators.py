class OtherFieldValidatorInSerializer:
    """
        A validator to be inherited from, that will give use the
        possibility of validate two fields.
        More exaplanation on comments along the code.

        TODO: Easily extensible to a list of fields

    USAGE EXAMPLE:
        (For a model that has to fields, date_start and date_end)

    In the serializer definition, we can have something like:

    from .validators import EndDateValidator
    class JobSerializer(serializers.ModelSerializer):
        class Meta:
            model = Job
            fields = '__all__'
            extra_kwargs = {
                'date_end': {'validators': [EndDateValidator('date_start')]},
            }
    """

    #### This part is the same for all validators ####

    def __init__(self, other_field):
        self.other_field = other_field # name of parameter

    def set_context(self, serializer_field):
        self.serializer_field = serializer_field # name of field where validator is defined

    def make_validation(self,field, other_field):
        pass

    def __call__(self, value):
        field = value
        serializer = self.serializer_field.parent # serializer of model

        try:
            # If <other_field> is not provided, here we will obtain the error
            # django.utils.datastructures.MultiValueDictKeyError: <'other_field'>
            # But we do not want to fail with that error. We want to fail for
            # example if it is a requiered field, with "This field is required"
            # If it is not a required field, and it was not provided, it does
            # not have sense to validate against, so we skip this anyway.
            raw_other_field = serializer.initial_data[self.other_field] # data del otro campo
            # Run validators from other_field before running this one. If it
            # does not pass the validations, it does not have sense to run
            # current. So we have to first fix the other field.
            other_field = serializer.fields[self.other_field].run_validation(raw_other_field)
        #except ValidationError:
        except:
            # if date_start is incorrect or was not provided in initial data
            # (sended in post api call for example) we will omit validating range
            return

    #### Here is the only part that changes ####

        # We MUST override this function
        self.make_validation(field,other_field)


