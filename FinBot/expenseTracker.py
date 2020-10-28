from FinBot import functions
from FinBot import helper
from FinBot import predictor
from FinBot.models import UserDetails

val=""

order = []
message_order = []


def tracker (statement, user_id):

	domain_tokens, maxlen, num_features = helper.get_dialog_options()
	prediction, amount = predictor.predict_intent(statement)

	amount_req = (
		prediction=='intent_housing' or 
		prediction=='intent_transportation' or
		prediction=='intent_food' or 
		prediction=='intent_recreation' or 
		prediction=='intent_healthcare' or 
		prediction=='intent_utilities' or 
		prediction=='intent_miscellaneous')


	if prediction is None:
		text_response = helper.generate_utter('utter_repeat_again')

	else:
		utterance_token = domain_tokens[prediction]
	
		state = helper.get_dialog_state()
		user_id_1=1

		if state is not None:
			pass
		else:
			state = dict({user_id_1: []})

		x_test = state[user_id_1]
		x_test.append(utterance_token)

		if len(x_test) > maxlen:
			x_test = x_test[-maxlen:]

		class_predicted, action_predicted = predictor.predict_action(domain_tokens, maxlen, num_features, x_test)

		text_response = helper.get_utterance(domain_tokens, action_predicted)
		val = text_response
		
		state[user_id_1] = x_test

		order.append(class_predicted)
		message_order.append(statement)

		if (amount == 0 and (amount_req)) :
			#ask for amount in next utterance
			text_response = "Please enter the amount you spent on this purchase."
			return text_response

		user_obj= UserDetails.objects.filter(pk = user_id)[0]

		if (order[len(order)-1] == 'utter_check'):

			if (order[len(order)-2] == 'utter_ask_price'):
				a = user_obj.account_balance
				if (amount <= a):
					return "Sure! You have enough funds to make this purchase."
				else:
					return "Sorry, you do not have enough funds to make this purchase."

			else:
				prediction, amt = predictor.predict_intent(message_order[len(message_order)-2])
				
				utterance_token = domain_tokens[prediction]
	
				state = helper.get_dialog_state()
				if state is not None:
					pass
				else:
					state = dict({user_id_1: []})

				x_test = state[user_id_1]
				x_test.append(utterance_token)

				if len(x_test) > maxlen:
					x_test = x_test[-maxlen:]

				class_predicted, action_predicted = predictor.predict_action(domain_tokens, maxlen, num_features, x_test)

				text_response = helper.get_utterance(domain_tokens, action_predicted)
				
				state[user_id_1] = x_test

	
				if (order[len(order)-2] == 'utter_housing'):
					functions.housing(user_obj, amount)
				
				if (order[len(order)-2] == 'utter_transportation'):
					functions.transportation(user_obj, amount)
				
				if (order[len(order)-2] == 'utter_food'):
					functions.food(user_obj, amount)
				
				if (order[len(order)-2] == 'utter_recreation'):
					functions.recreation(user_obj, amount)
				
				if (order[len(order)-2] == 'utter_healthcare'):
					functions.healthcare(user_obj, amount)
				
				if (order[len(order)-2] == 'utter_utilities'):
					functions.utilities(user_obj, amount)
				
				if (order[len(order)-2] == 'utter_miscellaneous'):
					functions.miscellaneous(user_obj, amount)

				
				text_response = (text_response.replace("__", "Rupees " + str(amount)))

				return text_response
				

		if action_predicted is not None:
			x_test.append(action_predicted)

		if (class_predicted == 'utter_account_balance'):
			amount = functions.account_balance(user_obj)

		if (class_predicted == 'utter_total_expenditure'):
			amount = functions.total_expenditure(user_obj)

		if (class_predicted == 'utter_check'):
			a = user_obj.account_balance
			if (amount <= a):
				return "Sure! You have enough funds to make this purchase"
			else:
				return "Sorry, you do not have enough funds to make this purchase."
		
		if (class_predicted == 'utter_housing'):
			functions.housing(user_obj, amount)
		
		if (class_predicted == 'utter_transportation'):
			functions.transportation(user_obj, amount)
		
		if (class_predicted == 'utter_food'):
			functions.food(user_obj, amount)
		
		if (class_predicted == 'utter_recreation'):
			functions.recreation(user_obj, amount)
		
		if (class_predicted == 'utter_healthcare'):
			functions.healthcare(user_obj, amount)
		
		if (class_predicted == 'utter_utilities'):
			functions.utilities(user_obj, amount)
		
		if (class_predicted == 'utter_miscellaneous'):
			functions.miscellaneous(user_obj, amount)
		
		if (class_predicted == 'utter_monthly_savings'):
			functions.monthly_savings(user_obj)

		text_response = (text_response.replace("__", "Rupees " + str(amount)))
		
		helper.save_dialog_state(state)

	return text_response