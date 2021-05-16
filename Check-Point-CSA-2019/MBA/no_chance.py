from z3 import *
import base64

eq_list_found = True



def ModelToFlagPrint(model_inst):
	order = [0x0E, 0x09, 0x17, 0x21, 0x02, 0x16, 0x00, 0x01, 0x07, 0x04, 0x05, 0x0B, 0x15, 0x0D, 0x0A, 0x07, 0x8, 0x0B, 0x0F, 0x06, 0x10, 0x0C, 0x20, 0x0A, 0x07, 0x0C, 0x0D, 0x0E, 0x0B, 0x19, 0x0B, 0x02, 0x00, 0x00, 0x0A, 0x03]
	raw_str = ''
	for i in order:
		raw_str += chr(model_inst[X[int(i)]].as_long())
	print(base64.b64decode((raw_str + '=' ).encode('utf-8')))


f = open(r'fs/bin_secret', 'rb')
buf = f.read()

X = [Int('x%s' % i) for i in range(34)]

constraints = []
for var in X:
	constraints.append(Or(And(var >= 65, var <= 90), And(var >= 97, var <= 122), And(var >= 48, var <= 57), var == 43, var == 47, var == 61))
	#constraints.append(var >= 90)
	#constraints.append(var >= 32)
	#constraints.append(var <= 126)

if not eq_list_found: # Shorten execution times from the second run on...
	f_offset = 0
	eq_list = []
	while buf[f_offset] != 0x2E or buf[f_offset+1] != 0x2E:
		eq_str = ''
		valid_eq = True
		for eq_offset in range(10):
			if eq_offset % 2 == 0:
				dec_var = int(buf[f_offset + eq_offset])
				if dec_var > 33:
					valid_eq = False
					break
				eq_str += 'X[' + str(dec_var) + ']'
				#print(buf[f_offset + eq_offset], end='')
			else:
				if buf[f_offset + eq_offset] == 0XFD:
					eq_str += '-'
					#print(' - ', end='')
				elif buf[f_offset + eq_offset] == 0XFE:
					eq_str += '*'
					#print(' * ', end='')
				elif buf[f_offset + eq_offset] == 0XFF:
					eq_str += '+'
					#print(' + ', end='')
				elif buf[f_offset + eq_offset] == 0X8A:
					eq_str += '=='
					#print(' = ', end='')
		f_offset += 10
		agg_res = 0
		if valid_eq:
			for res_offset in range(8):
				agg_res += buf[f_offset + res_offset] << (res_offset * 8)
		eq_str += str(int(agg_res))
		f_offset += 8
		if valid_eq:
			eq_list.append(eq_str)
	eq_list_to_rem = []
	for ind, eq in enumerate(eq_list):
		s = Solver() 
		for const in constraints:
			s.add(const)
		exec('s.add(' + eq + ')')
		if s.check() == unsat:
			print('removing ' + eq + ' ...')
			eq_list_to_rem.append(eq)
		print('Progrss: ' + str(ind + 1) + '/' + str(len(eq_list)))
	for eq in eq_list_to_rem:
		eq_list.remove(eq)
else:
	eq_list = ['X[1]-X[11]-X[17]+X[17]+X[30]==0', 'X[3]+X[5]-X[6]-X[0]+X[11]==16', 'X[26]+X[12]-X[9]-X[23]-X[31]==64', 'X[26]*X[2]+X[27]-X[5]*X[7]==103', 'X[27]-X[21]-X[21]+X[25]+X[20]==1', 'X[32]-X[1]+X[25]-X[9]+X[26]==0', 'X[28]+X[1]-X[23]-X[4]-X[11]==73', 'X[16]-X[8]*X[8]+X[1]*X[26]==126', 'X[30]+X[28]*X[33]-X[18]*X[8]==255', 'X[7]-X[25]+X[22]+X[3]+X[15]==32', 'X[8]*X[20]+X[12]-X[11]*X[24]==127', 'X[17]*X[24]-X[18]-X[13]*X[19]==253', 'X[14]+X[6]+X[7]-X[12]-X[8]==2', 'X[9]*X[19]+X[3]-X[24]*X[6]==127', 'X[0]+X[30]-X[20]+X[12]-X[11]==16', 'X[26]+X[2]-X[1]+X[24]+X[24]==2', 'X[16]+X[32]-X[3]-X[18]-X[5]==1', 'X[28]-X[0]-X[19]+X[8]-X[11]==132', 'X[29]-X[20]+X[6]+X[7]-X[25]==34', 'X[17]+X[29]-X[23]-X[22]-X[18]==48', 'X[29]*X[0]-X[32]*X[31]-X[14]==255', 'X[30]-X[31]+X[5]+X[20]-X[1]==2', 'X[19]+X[0]-X[10]-X[25]-X[27]==13', 'X[9]+X[26]-X[25]+X[16]-X[20]==0', 'X[15]*X[7]-X[11]*X[8]+X[30]==245', 'X[2]*X[24]-X[31]*X[32]-X[27]==207', 'X[22]+X[15]+X[8]-X[11]-X[30]==32', 'X[7]-X[15]+X[5]-X[11]+X[12]==0']

equations = eq_list

'''
s = Solver()
s.add(X[0] + X[1] == 5)
print(type(s.check()))
print(s.check())
if s.check().__repr__() == 'sat':
	print('aight')
'''

knowns = [X[14] == ord('Q'),
X[9] == ord('1'),
X[23] == ord('N'),
X[33] == ord('B'),
X[2] == ord('e')]

X_wo_knowns = X[0:2] + X[3:9] + X[10:14] + X[15:23] + X[24:33]
s = Solver()
for const in constraints:
	s.add(const)
for known in knowns:
	s.add(known)
red_equations = equations[10:14] + equations[21:28]
print(red_equations)
for eq in red_equations:
	exec('s.add(' + eq + ')')
print(s)	
while s.check() == sat:
	print('Still satisfiable')
	tmp_model = s.model()
	ModelToFlagPrint(tmp_model)
	restrict_str = ''
	for var in X_wo_knowns:
		var_str = var.__repr__()
		restrict_str += 'X[' + var_str[1:] + '] != tmp_model[X[' + var_str[1:] + ']], '
	restrict_str = restrict_str[:-2]
	exec('s.add(Or(' + restrict_str + '))')


#def little_to_big(num)