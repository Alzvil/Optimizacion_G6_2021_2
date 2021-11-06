from gurobipy import GRB, Model, quicksum

m = Model('Optimizacion de recursos hospitalarios')
M = 10^(60)

#max 108.750.000

#=====CONJUNTOS=====
i_personal = ['enf', 'sec', 'doc', 'cirj', 'ten']
f_rubros = ['adm', 'urg', 'clin', 'pab']
c_contratos = ['c1', 'c2', 'c3']
n_insumos = ['bisturi', 'pinzas', 'papel']
d_medicamentos = ['parac', 'ibup', 'queti', 'vit']
b_infraestructuras = ['box1', 'box2', 'box3', 'box4']
l_laboratorios = ['lab1', 'lab2', 'lab3']
v_bodegas = ['bod1', 'bod2']
t_periodo = ['ene', 'feb', 'mar', 'abr', 'may']

#=====PARAMETROS=====
personal_H = {
    'enf' : {
        ('ene', 'c1') : 500000, ('feb', 'c1') : 500000, ('mar', 'c1') : 500000, ('abr', 'c1') : 500000, ('may', 'c1') : 500000,
        ('ene', 'c2') : 600000, ('feb', 'c2') : 600000, ('mar', 'c2') : 600000, ('abr', 'c2') : 600000, ('may', 'c2') : 600000,
        ('ene', 'c3') : 700000, ('feb', 'c3') : 700000, ('mar', 'c3') : 700000, ('abr', 'c3') : 700000, ('may', 'c3') : 700000,
        },
    'sec' : {
        ('ene', 'c1') : 350000, ('feb', 'c1') : 350000, ('mar', 'c1') : 350000, ('abr', 'c1') : 350000, ('may', 'c1') : 350000,
        ('ene', 'c2') : 350000, ('feb', 'c2') : 350000, ('mar', 'c2') : 350000, ('abr', 'c2') : 350000, ('may', 'c2') : 350000,
        ('ene', 'c3') : 350000, ('feb', 'c3') : 350000, ('mar', 'c3') : 350000, ('abr', 'c3') : 350000, ('may', 'c3') : 350000,
        },
    'doc' : {
        ('ene', 'c1') : 800000, ('feb', 'c1') : 800000, ('mar', 'c1') : 800000, ('abr', 'c1') : 800000, ('may', 'c1') : 800000,
        ('ene', 'c2') : 850000, ('feb', 'c2') : 850000, ('mar', 'c2') : 850000, ('abr', 'c2') : 850000, ('may', 'c2') : 850000,
        ('ene', 'c3') : 900000, ('feb', 'c3') : 900000, ('mar', 'c3') : 900000, ('abr', 'c3') : 900000, ('may', 'c3') : 900000,
        },
    'cirj' : {
        ('ene', 'c1') : 1000000, ('feb', 'c1') : 1000000, ('mar', 'c1') : 1000000, ('abr', 'c1') : 1000000, ('may', 'c1') : 1000000,
        ('ene', 'c2') : 1250000, ('feb', 'c2') : 1250000, ('mar', 'c2') : 1250000, ('abr', 'c2') : 1250000, ('may', 'c2') : 1250000,
        ('ene', 'c3') : 1500000, ('feb', 'c3') : 1500000, ('mar', 'c3') : 1500000, ('abr', 'c3') : 1500000, ('may', 'c3') : 1500000,
        },
    'ten' : {
        ('ene', 'c1') : 350000, ('feb', 'c1') : 350000, ('mar', 'c1') : 350000, ('abr', 'c1') : 450000, ('may', 'c1') : 550000,
        ('ene', 'c2') : 350000, ('feb', 'c2') : 350000, ('mar', 'c2') : 350000, ('abr', 'c2') : 450000, ('may', 'c2') : 550000,
        ('ene', 'c3') : 350000, ('feb', 'c3') : 350000, ('mar', 'c3') : 350000, ('abr', 'c3') : 450000, ('may', 'c3') : 550000,
        }
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
    'bisturi' : {'ene' : 50, 'feb' : 50, 'mar' : 50, 'abr' : 50, 'may' : 50}, 
    'pinzas' : {'ene' : 60, 'feb' : 60, 'mar' : 60, 'abr' : 60, 'may' : 60}, 
    'papel' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}
}
insumos_E = {
    'bisturi' : {
        ('ene', 'bod1') : 325, ('feb', 'bod1') : 325, ('mar', 'bod1') : 325, ('abr', 'bod1') : 325, ('may', 'bod1') : 325,
        ('ene', 'bod2') : 225, ('feb', 'bod2') : 225, ('mar', 'bod2') : 225, ('abr', 'bod2') : 225, ('may', 'bod2') : 225,
        },
    'pinzas' : {
        ('ene', 'bod1') : 325, ('feb', 'bod1') : 325, ('mar', 'bod1') : 325, ('abr', 'bod1') : 325, ('may', 'bod1') : 325,
        ('ene', 'bod2') : 325, ('feb', 'bod2') : 325, ('mar', 'bod2') : 325, ('abr', 'bod2') : 325, ('may', 'bod2') : 325,
        },
    'papel' : {
        ('ene', 'bod1') : 300, ('feb', 'bod1') : 300, ('mar', 'bod1') : 300, ('abr', 'bod1') : 300, ('may', 'bod1') : 300,
        ('ene', 'bod2') : 200, ('feb', 'bod2') : 200, ('mar', 'bod2') : 200, ('abr', 'bod2') : 200, ('may', 'bod2') : 200,
        }
}
insumos_L = {
    'ene' : 1000000, 'feb' : 1000000, 'mar' : 1000000, 'abr' : 1000000, 'may' : 1000000
}
insumos_Ii = {
    'bisturi' : {'ene' : 0, 'feb' : 0, 'mar' : 0, 'abr' : 0, 'may' : 0}, 
    'pinzas' : {'ene' : 0, 'feb' : 0, 'mar' : 0, 'abr' : 0, 'may' : 0}, 
    'papel' : {'ene' : 0, 'feb' : 0, 'mar' : 0, 'abr' : 0, 'may' : 0}
}
insumos_Ai = {
    'bisturi' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}, 
    'pinzas' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}, 
    'papel' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}
}
insumos_CFi = {
    'bisturi' : {
        ('ene', 'bod1') : 100, ('feb', 'bod1') : 100, ('mar', 'bod1') : 100, ('abr', 'bod1') : 100, ('may', 'bod1') : 100,
        ('ene', 'bod2') : 100, ('feb', 'bod2') : 100, ('mar', 'bod2') : 100, ('abr', 'bod2') : 100, ('may', 'bod2') : 100,
        },
    'pinzas' : {
        ('ene', 'bod1') : 100, ('feb', 'bod1') : 100, ('mar', 'bod1') : 100, ('abr', 'bod1') : 100, ('may', 'bod1') : 100,
        ('ene', 'bod2') : 100, ('feb', 'bod2') : 100, ('mar', 'bod2') : 100, ('abr', 'bod2') : 100, ('may', 'bod2') : 100,
        },
    'papel' : {
        ('ene', 'bod1') : 100, ('feb', 'bod1') : 100, ('mar', 'bod1') : 100, ('abr', 'bod1') : 100, ('may', 'bod1') : 100,
        ('ene', 'bod2') : 100, ('feb', 'bod2') : 100, ('mar', 'bod2') : 100, ('abr', 'bod2') : 100, ('may', 'bod2') : 100,
        }
}
medicamentos_Q = {
    'parac' : {
        ('ene', 'lab1') : 750, ('feb', 'lab1') : 750, ('mar', 'lab1') : 750, ('abr', 'lab1') : 750, ('may', 'lab1') : 750,
        ('ene', 'lab2') : 800, ('feb', 'lab2') : 800, ('mar', 'lab2') : 800, ('abr', 'lab2') : 800, ('may', 'lab2') : 800,
        ('ene', 'lab3') : 800, ('feb', 'lab3') : 800, ('mar', 'lab3') : 800, ('abr', 'lab3') : 800, ('may', 'lab3') : 800
        },
    'ibup' : {
        ('ene', 'lab1') : 800, ('feb', 'lab1') : 800, ('mar', 'lab1') : 800, ('abr', 'lab1') : 800, ('may', 'lab1') : 800,
        ('ene', 'lab2') : 750, ('feb', 'lab2') : 750, ('mar', 'lab2') : 750, ('abr', 'lab2') : 750, ('may', 'lab2') : 750,
        ('ene', 'lab3') : 700, ('feb', 'lab3') : 700, ('mar', 'lab3') : 700, ('abr', 'lab3') : 700, ('may', 'lab3') : 700
        },
    'queti' : {
        ('ene', 'lab1') : 1950, ('feb', 'lab1') : 1950, ('mar', 'lab1') : 1950, ('abr', 'lab1') : 1950, ('may', 'lab1') : 1950,
        ('ene', 'lab2') : 1950, ('feb', 'lab2') : 1950, ('mar', 'lab2') : 1950, ('abr', 'lab2') : 1950, ('may', 'lab2') : 1950,
        ('ene', 'lab3') : 1500, ('feb', 'lab3') : 1500, ('mar', 'lab3') : 1500, ('abr', 'lab3') : 1500, ('may', 'lab3') : 1500
        },
    'vit' : {
        ('ene', 'lab1') : 750, ('feb', 'lab1') : 750, ('mar', 'lab1') : 750, ('abr', 'lab1') : 750, ('may', 'lab1') : 750,
        ('ene', 'lab2') : 500, ('feb', 'lab2') : 500, ('mar', 'lab2') : 500, ('abr', 'lab2') : 500, ('may', 'lab2') : 500,
        ('ene', 'lab3') : 650, ('feb', 'lab3') : 650, ('mar', 'lab3') : 650, ('abr', 'lab3') : 650, ('may', 'lab3') : 650
        }
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
    'parac' : {'ene' : 0, 'feb' : 0, 'mar' : 0, 'abr' : 0, 'may' : 0}, 
    'ibup' : {'ene' : 0, 'feb' : 0, 'mar' : 0, 'abr' : 0, 'may' : 0},
    'queti' : {'ene' : 0, 'feb' : 0, 'mar' : 0, 'abr' : 0, 'may' : 0},
    'vit' : {'ene' : 0, 'feb' : 0, 'mar' : 0, 'abr' : 0, 'may' : 0}
}
medicamentos_Am = {
    'parac' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}, 
    'ibup' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}, 
    'queti' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100},
    'vit' : {'ene' : 100, 'feb' : 100, 'mar' : 100, 'abr' : 100, 'may' : 100}
}
medicamentos_CFm = {
    'parac' : {
        ('ene', 'lab1') : 100, ('feb', 'lab1') : 100, ('mar', 'lab1') : 100, ('abr', 'lab1') : 100, ('may', 'lab1') : 100,
        ('ene', 'lab2') : 100, ('feb', 'lab2') : 100, ('mar', 'lab2') : 100, ('abr', 'lab2') : 100, ('may', 'lab2') : 100,
        ('ene', 'lab3') : 100, ('feb', 'lab3') : 100, ('mar', 'lab3') : 100, ('abr', 'lab3') : 100, ('may', 'lab3') : 100
        },
    'ibup' : {
        ('ene', 'lab1') : 100, ('feb', 'lab1') : 100, ('mar', 'lab1') : 100, ('abr', 'lab1') : 100, ('may', 'lab1') : 100,
        ('ene', 'lab2') : 100, ('feb', 'lab2') : 100, ('mar', 'lab2') : 100, ('abr', 'lab2') : 100, ('may', 'lab2') : 100,
        ('ene', 'lab3') : 100, ('feb', 'lab3') : 100, ('mar', 'lab3') : 100, ('abr', 'lab3') : 100, ('may', 'lab3') : 100
        },
    'queti' : {
        ('ene', 'lab1') : 100, ('feb', 'lab1') : 100, ('mar', 'lab1') : 100, ('abr', 'lab1') : 100, ('may', 'lab1') : 100,
        ('ene', 'lab2') : 100, ('feb', 'lab2') : 100, ('mar', 'lab2') : 100, ('abr', 'lab2') : 100, ('may', 'lab2') : 100,
        ('ene', 'lab3') : 100, ('feb', 'lab3') : 100, ('mar', 'lab3') : 100, ('abr', 'lab3') : 100, ('may', 'lab3') : 100
        },
    'vit' : {
        ('ene', 'lab1') : 100, ('feb', 'lab1') : 100, ('mar', 'lab1') : 100, ('abr', 'lab1') : 100, ('may', 'lab1') : 100,
        ('ene', 'lab2') : 100, ('feb', 'lab2') : 100, ('mar', 'lab2') : 100, ('abr', 'lab2') : 100, ('may', 'lab2') : 100,
        ('ene', 'lab3') : 100, ('feb', 'lab3') : 100, ('mar', 'lab3') : 100, ('abr', 'lab3') : 100, ('may', 'lab3') : 100
        }
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
            varA[personal, contrato, periodo] = m.addVar(vtype=GRB.INTEGER, name="varA_{}_{}_{}".format(personal, contrato, periodo))
    for rubro in f_rubros:
        varP[rubro, periodo] = m.addVar(vtype=GRB.CONTINUOUS, name="varP_{}_{}".format(rubro, periodo))
    for insumo in n_insumos:
        varS[insumo, periodo] = m.addVar(vtype=GRB.INTEGER, name="varS_{}_{}".format(insumo, periodo))
        varIi[insumo, periodo] = m.addVar(vtype=GRB.INTEGER, name="varIi_{}_{}".format(insumo, periodo))
        for bodega in v_bodegas:
            varG[insumo, bodega, periodo] = m.addVar(vtype=GRB.INTEGER, name="varG_{}_{}_{}".format(insumo, bodega, periodo))
            varSn[insumo, bodega, periodo] = m.addVar(lb=0, ub=1, vtype=GRB.BINARY, name="varSn_{}_{}_{}".format(insumo, bodega, periodo))
    for medicamento in d_medicamentos:
        varQ[medicamento, periodo] = m.addVar(vtype=GRB.INTEGER, name="varQ_{}_{}".format(medicamento, periodo))
        varIm[medicamento, periodo] = m.addVar(vtype=GRB.INTEGER, name="varIm_{}_{}".format(medicamento, periodo))
        for laboratorio in l_laboratorios:
            varM[medicamento, laboratorio, periodo] = m.addVar(vtype=GRB.INTEGER, name="varM_{}_{}_{}".format(medicamento, laboratorio, periodo))
            varSd[medicamento, laboratorio, periodo] = m.addVar(lb=0, ub=1, vtype=GRB.BINARY, name="varSd_{}_{}_{}".format(medicamento, laboratorio, periodo))

m.update()

#=====RESTRICCIONES=====

#A: Presupuesto funcionarios:
for periodo in t_periodo:
    for personal in i_personal:
        for rubro in f_rubros:
            m.addConstr(quicksum(personal_H[personal][(periodo, contrato)] * varA[personal, contrato, periodo] for contrato in c_contratos) \
                <= varP[rubro, periodo], 'presuFunc_{}_{}_{}'.format(personal, rubro, periodo))

#B: Presupuesto por tipo no exceder total:
for periodo in t_periodo:
    m.addConstr(quicksum(varP[rubro, periodo] for rubro in f_rubros) <= personal_A[periodo], \
        'presuRubr_{}'.format(periodo))

#C: Minimo de funcionarios:
for periodo in t_periodo:
    for personal in i_personal:
        for rubro in f_rubros:
            m.addConstr(personal_V[rubro][periodo] <= quicksum(varA[personal, contrato, periodo] \
                for contrato in c_contratos), 'minFunRub_{}_{}_{}'.format(personal, rubro, periodo))

#D: Presupuesto insumos:
for periodo in t_periodo:
    for insumo in n_insumos:
        m.addConstr(varIi[insumo, periodo] * insumos_Ai[insumo][periodo] + quicksum( \
            varG[insumo, bodega, periodo] * insumos_E[insumo][(periodo, bodega)] for bodega in v_bodegas) \
            <= insumos_L[periodo], 'presuInsu_{}_{}'.format(insumo, periodo))

#E: Minimo insumos:
for periodo in t_periodo:
    for insumo in n_insumos:
        m.addConstr(insumos_G[insumo][periodo] <= quicksum(varG[insumo, bodega, periodo] \
            for bogeda in v_bodegas), 'minimInsu_{}_{}'.format(insumo, periodo))

#F: Binaria insumos:
for periodo in t_periodo:
    for insumo in n_insumos:
        for bodega in v_bodegas:
            m.addConstr(varG[insumo, bodega, periodo] <= GRB.INFINITY * varSn[insumo, bodega, periodo], \
                'binarInsu_{}_{}_{}'.format(periodo, insumo, bodega))

#G: Presupuesto medicamentos:
for periodo in t_periodo:
    m.addConstr(quicksum(varIm[medicamento, periodo] * medicamentos_Am[medicamento][periodo] + quicksum( \
        varM[medicamento, laboratorio, periodo] * medicamentos_Q[medicamento][(periodo, laboratorio)] \
        for laboratorio in l_laboratorios) for medicamento in d_medicamentos) <= medicamentos_Z[periodo], \
        'presMedic_{}'.format(periodo))

#H: Minimo medicamentos:
for periodo in t_periodo:
    for medicamento in d_medicamentos:
        m.addConstr(medicamentos_O[medicamento][periodo] <= quicksum(varM[medicamento, laboratorio, periodo] \
            for laboratorio in l_laboratorios), 'minimInsu_{}_{}'.format(medicamento, periodo))

#F: Binaria medicamentos:
for periodo in t_periodo:
    for medicamento in d_medicamentos:
        for laboratorio in l_laboratorios:
            m.addConstr(varM[medicamento, laboratorio, periodo] <= GRB.INFINITY * varSd[medicamento, laboratorio, periodo], \
                'binarInsu_{}_{}_{}'.format(periodo, insumo, bodega))

#J-K: Inv medicamentos:
for periodo_index, periodo in enumerate(t_periodo):
    for medicamento in d_medicamentos:
        if periodo_index == 0:
            m.addConstr(medicamentos_Im[medicamento][periodo] + quicksum(varM[medicamento, laboratorio, periodo] for laboratorio in l_laboratorios) \
                == varQ[medicamento, periodo] + medicamentos_Im[medicamento][periodo], 'invMedIni_{}_{}'.format(medicamento, periodo))
        else:
            m.addConstr(medicamentos_Im[medicamento][t_periodo[periodo_index-1]] + quicksum(varM[medicamento, laboratorio, periodo] for laboratorio in l_laboratorios) \
                == varQ[medicamento, periodo] + medicamentos_Im[medicamento][periodo], 'invMedicm_{}_{}'.format(medicamento, periodo))

#L-M: Inv insumos:
for periodo_index, periodo in enumerate(t_periodo):
    for insumo in n_insumos:
        if periodo_index == 0:
            m.addConstr(insumos_Ii[insumo][periodo] + quicksum(varG[insumo, bodega, periodo] for bodega in v_bodegas) \
                == varS[insumo, periodo] + insumos_Ii[insumo][periodo], 'invInsIni_{}_{}'.format(insumo, periodo))
        else:
            m.addConstr(insumos_Ii[insumo][t_periodo[periodo_index-1]] + quicksum(varG[insumo, bodega, periodo] for bodega in v_bodegas) \
                == varS[insumo, periodo] + insumos_Ii[insumo][periodo], 'invInsumo_{}_{}'.format(insumo, periodo))

#=====FUNCION OBJETIVO=====
sum_personal = quicksum(varP[rubro, periodo] for rubro in f_rubros)
sum_insumos = quicksum(insumos_Ai[insumo][periodo] * insumos_Ii[insumo][periodo] + quicksum( \
                insumos_E[insumo][(periodo, bodega)] * varG[insumo, bodega, periodo] + \
                insumos_CFi[insumo][(periodo, bodega)] * varSn[insumo, bodega, periodo] \
                for bodega in v_bodegas) for insumo in n_insumos)
sum_medicamentos = quicksum(medicamentos_Am[medicamento][periodo] * medicamentos_Im[medicamento][periodo] + quicksum( \
                    medicamentos_Q[medicamento][(periodo, laboratorio)] * varM[medicamento, laboratorio, periodo] + \
                    medicamentos_CFm[medicamento][(periodo, laboratorio)] * varSd[medicamento, laboratorio, periodo] \
                    for laboratorio in l_laboratorios) for medicamento in d_medicamentos)

objetivo = quicksum(sum_personal + sum_insumos + sum_medicamentos for periodo in t_periodo)

m.setObjective(objetivo, GRB.MINIMIZE)

#OPTIMIZACION
m.optimize()

m.printAttr("X")
print("\n-------------\n")
for constr in m.getConstrs():
    print(constr, constr.getAttr("slack"))