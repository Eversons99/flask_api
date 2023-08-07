model = {
   "alvocom" : ['host', 'serial-number', 'pon', 'id']
}

def check_fields(data_list, model_name):
   if model_name not in model.keys():
      return {
         "error": 'Please inform a valid model_name.'
      }

   body_params = data_list.keys()
   missing_params = []

   for param in model[model_name]:
      if param not in body_params:
         missing_params.append(param)
      else:
         if data_list[param].strip() == '':
            missing_params.append(param)

   if len(missing_params) != 0:
      return {
         "error": 
            f'Inform the parameter(s): {", " .join(missing_params)}'
         }

   return {
      "message": "Success, all fields are correct"
   }