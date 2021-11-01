from gurobipy import GRB, Model, quicksum

m = Model('Optimizacion de recursos hospitalarios')

#max 108.750.000

#=====CONJUNTOS=====
i_personal = ['enf', 'sec', 'doc', 'cirj', 'ten']
f_rubros = ['adm', 'urg', 'clin', 'pab']
c_contratos = ['c1', 'c2', 'c3', 'c4']
n_insumos = ['visturi', 'pinzas', 'papel']
d_medicamentos = ['parac', 'ibup', 'queti', 'vit']
b_infraestructuras = ['box1', 'box2', 'box3', 'box4']
l_laboratorios = ['lab1', 'lab2', 'lab3']
v_bodegas = ['bod1', 'bod2']
t_periodo = ['ene', 'feb', 'mar', 'abr', 'may']

#=====PARAMETROS=====
personal_H = {
    'enf' : {('ene', 'c2') : 600000, ('feb', 'c2') : 600000, ('mar', 'c2') : 600000, ('abr', 'c2') : 600000, ('may', 'c3') : 850000},
    'sec' : {('ene', 'c1') : 350000, ('feb', 'c1') : 350000, ('mar', 'c1') : 350000, ('abr', 'c1') : 350000, ('may', 'c1') : 350000},
    'doc' : {('ene', 'c3') : 850000, ('feb', 'c3') : 850000, ('mar', 'c3') : 850000, ('abr', 'c3') : 850000, ('may', 'c3') : 850000},
    'cirj' : {('ene', 'c4') : 1000000, ('feb', 'c4') : 1000000, ('mar', 'c4') : 1000000, ('abr', 'c4') : 1000000, ('may', 'c4') : 1000000},
    'ten' : {('ene', 'c1') : 350000, ('feb', 'c1') : 350000, ('mar', 'c1') : 350000, ('abr', 'c2') : 600000, ('may', 'c2') : 600000}
}
personal_V = {
    'adm' : {'ene' : 12, 'feb' : 12, 'mar' : 12, 'abr' : 12, 'may' : 12}, 
    'urg' : {'ene' : 50, 'feb' : 50, 'mar' : 50, 'abr' : 75, 'may' : 75},
    'clin' : {'ene' : 50, 'feb' : 50, 'mar' : 50, 'abr' : 70, 'may' : 70}, 
    'pab' : {'ene' : 15, 'feb' : 15, 'mar' : 15, 'abr' : 5, 'may' : 5}, 
}
personal_A = {
    'ene' : 108750000, 'feb' : 108750000, 'mar' : 108750000, 'abr' : 108750000, 'may' : 108750000
}
insumos_G = {
    'visturi' : {'ene' : 50, 'feb' : 50, 'mar' : 50, 'abr' : 50, 'may' : 50}, 
    'pinzas' : {'ene' : 60, 'feb' : 60, 'mar' : 60, 'abr' : 60, 'may' : 60}, 
    'papel' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}
}
insumos_E = {
    'visturi' : {('ene', 'bod1') : 800, ('feb', 'bod1') : 800, ('mar', 'bod1') : 800, ('abr', 'bod1') : 800, ('may', 'bod1') : 800},
    'pinzas' : {('ene', 'bod1') : 750, ('feb', 'bod1') : 750, ('mar', 'bod1') : 750, ('abr', 'bod1') : 750, ('may', 'bod1') : 750},
    'papel' : {('ene', 'bod2') : 500, ('feb', 'bod2') : 500, ('mar', 'bod2') : 500, ('abr', 'bod2') : 500, ('may', 'bod2') : 500}
}
insumos_L = {
    'ene' : 1000000, 'feb' : 1000000, 'mar' : 1000000, 'abr' : 1000000, 'may' : 1000000
}
insumos_Ii = {
    'visturi' : 0, 'pinzas' : 0, 'papel' : 0
}
insumos_Ai = {
    'visturi' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}, 
    'pinzas' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}, 
    'papel' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}
}
insumos_CFi = {
    'visturi' : {('ene', 'bod1') : 100, ('feb', 'bod1') : 100, ('mar', 'bod1') : 100, ('abr', 'bod1') : 100, ('may', 'bod1') : 100}, 
    'pinzas' : {('ene', 'bod1') : 100, ('feb', 'bod1') : 100, ('mar', 'bod1') : 100, ('abr', 'bod1') : 100, ('may', 'bod1') : 100}, 
    'papel' : {('ene', 'bod2') : 100, ('feb', 'bod2') : 100, ('mar', 'bod3') : 100, ('abr', 'bod3') : 100, ('may', 'bod3') : 100}
}
medicamentos_Q = {
    'parac' : {('ene', 'lab2') : 800, ('feb', 'lab2') : 800, ('mar', 'lab2') : 800, ('abr', 'lab2') : 800, ('may', 'lab2') : 800},
    'ibup' : {('ene', 'lab2') : 750, ('feb', 'lab2') : 750, ('mar', 'lab2') : 750, ('abr', 'lab2') : 750, ('may', 'lab2') : 750},
    'queti' : {('ene', 'lab2') : 1950, ('feb', 'lab2') : 1950, ('mar', 'lab2') : 1950, ('abr', 'lab2') : 1950, ('may', 'lab2') : 1950},
    'vit' : {('ene', 'lab1') : 500, ('feb', 'lab1') : 500, ('mar', 'lab1') : 500, ('abr', 'lab1') : 500, ('may', 'lab1') : 500}
}
medicamentos_O = {
    'parac' : {'ene' : 50, 'feb' : 50, 'mar' : 50, 'abr' : 50, 'may' : 50}, 
    'ibup' : {'ene' : 60, 'feb' : 60, 'mar' : 60, 'abr' : 60, 'may' : 60}, 
    'queti' : {'ene' : 50, 'feb' : 50, 'mar' : 50, 'abr' : 50, 'may' : 50}, 
    'vit' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}
}
medicamentos_Z = {
    'ene' : 1000000, 'feb' : 1000000, 'mar' : 1000000, 'abr' : 1000000, 'may' : 1000000
}
medicamentos_Im = {
    'parac' : 0, 'ibup' : 0, 'queti' : 0, 'vit' : 0
}
medicamentos_Am = {
    'parac' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}, 
    'ibup' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}, 
    'queti' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100},
    'vit' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}
}
medicamentos_CFm = {
    'parac' : {('ene', 'lab2') : 100, ('feb', 'lab2') : 100, ('mar', 'lab2') : 100, ('abr', 'lab2') : 100, ('may', 'lab2') : 100}, 
    'ibup' : {('ene', 'lab2') : 100, ('feb', 'lab2') : 100, ('mar', 'lab2') : 100, ('abr', 'lab2') : 100, ('may', 'lab2') : 100}, 
    'queti' : {('ene', 'lab2') : 100, ('feb', 'lab2') : 100, ('mar', 'lab2') : 100, ('abr', 'lab2') : 100, ('may', 'lab2') : 100}, 
    'vit' : {('ene', 'lab1') : 100, ('feb', 'lab1') : 100, ('mar', 'lab1') : 100, ('abr', 'lab1') : 100, ('may', 'lab1') : 100}
}
infraestructura_Y = {
    'box1' : {'ene' : 350000, 'feb' : 350000, 'mar' : 350000, 'abr' : 350000, 'may' : 350000}, 
    'box2' : {'ene' : 350000, 'feb' : 350000, 'mar' : 350000, 'abr' : 350000, 'may' : 350000}, 
    'box3' : {'ene' : 350000, 'feb' : 350000, 'mar' : 350000, 'abr' : 350000, 'may' : 350000}, 
    'box4' : {'ene' : 350000, 'feb' : 350000, 'mar' : 350000, 'abr' : 350000, 'may' : 350000}
}

#=====PARAMETROS CONSTANTES=====

#=====VARIABLES DE DECISION=====
varA = {}
varP = {}
varG = {}
varS = {}
varM = {}
varQ = {}
varIi = {}
varIm = {}
varSn = {}
varSd = {}
varRa = {}
varHm = {}

for periodo in t_periodo:
    for personal in i_personal:
        for contrato in c_contratos:
            varA[personal, contrato, periodo] = m.addVar(vtype=GRB.INTERGER, name="varA_{}_{}_{}".format(personal, contrato, periodo))
    for rubro in f_rubros:
        varP[rubro, periodo] = m.addVar(vtype=GRB.CONTINUOUS, name="varP_{}_{}".format(rubro, periodo))
    for insumo in n_insumos:
        varS[insumo, periodo] = m.addVar(vtype=GRB.INTERGER, name="varS_{}_{}".format(insumo, periodo))
        varIi[insumo, periodo] = m.addVar(vtype=GRB.INTERGER, name="varIi_{}_{}".format(insumo, periodo))
        for bodega in v_bodegas:
            varG[insumo, bodega, periodo] = m.addVar(vtype=GRB.INTERGER, name="varG_{}_{}_{}".format(insumo, bodega, periodo))
    for medicamento in d_medicamentos:
        varQ[medicamento, periodo] = m.addVar(vtype=GRB.INTERGER, name="varQ_{}_{}".format(medicamento, periodo))
        varIm[medicamento, periodo] = m.addVar(vtype=GRB.INTERGER, name="varIm_{}_{}".format(medicamento, periodo))
        for laboratorio in l_laboratorios:
            varM[medicamento, laboratorio, periodo] = m.addVar(vtype=GRB.INTERGER, name="varM_{}_{}_{}".format(medicamento, laboratorio, periodo))

m.update()

#=====RESTRICCIONES=====

#A: Presupuesto funcionarios:
for periodo in t_periodo:
    for personal in i_personal:
        for rubro in f_rubros:
            m.addConstr(quicksum(personal_H[personal, (periodo, contrato)] * varA[personal, contrato, periodo] for contrato in c_contratos) \
                <= varP[rubro, periodo], 'presuFunc_{}_{}_{}'.format(personal, rubro, periodo))

#B: Presupuesto por tipo no exceder total:
for periodo in t_periodo:
    m.addConstr(quicksum(varP[rubro, periodo] for rubro in f_rubros) <= personal_A, 'presuRubr_{}'.format(periodo))

#C: Minimo de funcionarios:
for periodo in t_periodo:
    for personal in i_personal:
        for rubro in f_rubros:
            m.addConstr(personal_V[rubro, periodo] <= quicksum(varA[personal, contrato, periodo] for contrato in c_contratos), 'minFunRub_{}_{}_{}'.format(personal, rubro, periodo))

#D:

#J-K: Inv medicamentos:
for periodo_index, periodo in enumerate(t_periodo):
    for medicamento in d_medicamentos:
        if periodo_index == 0:
            m.addConstr(medicamentos_Im[medicamento, periodo] + quicksum(varM[medicamento, laboratorio, periodo] for laboratorio in l_laboratorios) \
                == varQ[medicamento, periodo] + medicamentos_Im[medicamento, periodo], 'invMedIni_{}_{}'.format(medicamento, periodo))
        else:
            m.addConstr(medicamentos_Im[medicamento, t_periodo[periodo_index-1]] + quicksum(varM[medicamento, laboratorio, periodo] for laboratorio in l_laboratorios) \
                == varQ[medicamento, periodo] + medicamentos_Im[medicamento, periodo], 'invMedicm_{}_{}'.format(medicamento, periodo))

#L-M: Inv insumos:
for periodo_index, periodo in enumerate(t_periodo):
    for insumo in n_insumos:
        if periodo_index == 0:
            m.addConstr(insumos_Ii[insumo, periodo] + quicksum(varG[insumo, bodega, periodo] for bodega in v_bodegas) \
                == varS[insumo, periodo] + insumos_Ii[insumo, periodo], 'invInsIni_{}_{}'.format(insumo, periodo))
        else:
            m.addConstr(insumos_Ii[insumo, t_periodo[periodo_index-1]] + quicksum(varG[insumo, bodega, periodo] for bodega in v_bodegas) \
                == varS[insumo, periodo] + insumos_Ii[insumo, periodo], 'invInsumo_{}_{}'.format(insumo, periodo))

#=====FUNCION OBJETIVO=====
sum_personal = quicksum(varP[rubro, periodo] for rubro in f_rubros)
sum_insumos = quicksum(insumos_Ai[insumo, periodo] * insumos_Ii[insumo, periodo] + quicksum( \
                insumos_E[insumo, (periodo, bodega)] * varG[insumo, bodega, periodo] + \
                insumos_CFi[insumo, (periodo, bodega)] * varSn[insumo, bodega, periodo] \
                for bodega in v_bodegas) for insumo in n_insumos)
sum_medicamentos = quicksum(medicamentos_Am[medicamento, periodo] * medicamentos_Im[medicamento, periodo] + quicksum( \
                    medicamentos_Q[medicamento, (periodo, laboratorio)] * varM[medicamento, laboratorio, periodo] + \
                    medicamentos_CFm[medicamento, (periodo, laboratorio)] * varSd[medicamento, laboratorio, periodo] \
                    for laboratorio in l_laboratorios) for medicamento in d_medicamentos)
sum_infraest = quicksum(infraestructura_Y[infraestructura, periodo] * varHm[infraestructura, periodo] \
                    for infraestructura in b_infraestructuras)

objetivo = quicksum(sum_personal + sum_insumos + sum_medicamentos + sum_infraest for periodo in t_periodo)

m.setObjective(objetivo, GRB.MAXIMIZE)

#OPTIMIZACION
m.optimize()

m.printAttr("X")
print("\n-------------\n")
for constr in m.getConstrs():
    print(constr, constr.getAttr("slack"))