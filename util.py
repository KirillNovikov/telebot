def check_correction_of_exam(answers,user_answers):
	num_of_q = len(answers)
	num_of_corr_a = 0
	message = []
	message.append('\nВаш ответ | Правильный ответ\n')
	for bs_ans in answers:
		count = 0
		for usr_ans in user_answers:
			if bs_ans[0] == usr_ans[0]:
				sign = '-'
				if bs_ans[1] == usr_ans[1]:
					num_of_corr_a += 1
					sign = '+'	
				st = '%s) (%s) %s | %s' % (bs_ans[0],sign, usr_ans[1], bs_ans[1])
				message.append(st)
				break
	
	inspiring_message = None
	points = (0.5 * num_of_corr_a,
		      0.90 * num_of_corr_a)
	if num_of_corr_a == num_of_q:
		inspiring_message = 'Великолепно!'
	elif num_of_corr_a > 0.8 * num_of_q:
		inspiring_message = 'Замечательно!'
	elif num_of_corr_a > 0.5 * num_of_q:
		inspiring_message = 'Хорошо!'
	else:
		inspiring_message = 'Ты можешь лучше!'

	message.append('')
	message.append(inspiring_message)
	message = '\n'.join(message)
	return (num_of_corr_a, num_of_q, message)

def answer_to_list(answers):
	result = answers.split(sep='\n')
	while not result[-1]: result.pop()
	while not result[0]: result = result[1:]
	for ind, a in enumerate(result):
		offset = a.index(' ')
		num_of_q = a[:offset]
		ans = a[offset+1:].lower().strip()
		result[ind] = (num_of_q, ans)
	return result
