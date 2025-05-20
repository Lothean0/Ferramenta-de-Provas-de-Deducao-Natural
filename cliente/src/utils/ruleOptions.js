export const ruleOptions = {
    axiom: {
        label: {
            EN: "Hypothesis",
            PT: "Hipótese",
        },
        needsAuxiliary: true,
        auxFormulaPlaceholder: {
            EN: "N/A",
            PT: "Indentificador da hipótese",
        },
    },
    implication_introduction: {
        label: {
            EN: "Implication Intro.",
            PT: "Intro. Implicação",
        },
        needsAuxiliary: false,
    },
    implication_elimination: {
        label: {
            EN: "Implication Elim.",
            PT: "Elim. Implicação",
        },
        needsAuxiliary: true,
        auxFormulaPlaceholder: {
            EN: "N/A",
            PT: 'Em "A->B" a eliminar, indique A:',
        },
    },
    conjunction_introduction: {
        label: {
            EN: "Conjunction Intro.",
            PT: "Intro. Conjunção",
        },
        needsAuxiliary: false,
    },
    conjunction_elimination_1: {
        label: {
            EN: "Conjunction Elim. 1",
            PT: "Elim. Conjunção 1",
        },
        needsAuxiliary: true,
        auxFormulaPlaceholder: {
            EN: "N/A",
            PT: 'Em "A/\\B" a eliminar, indique B:',
        },
    },
    conjunction_elimination_2: {
        label: {
            EN: "Conjunction Elim. 2",
            PT: "Elim. Conjunção 2",
        },
        needsAuxiliary: true,
        auxFormulaPlaceholder: {
            EN: "N/A",
            PT: 'Em "A/\\B" a eliminar, indique A:',
        },
    },
    disjunction_introduction_1: {
        label: {
            EN: "Disjunction Intro. 1",
            PT: "Intro. Disjunção 1",
        },
        needsAuxiliary: false,
    },
    disjunction_introduction_2: {
        label: {
            EN: "Disjunction Intro. 2",
            PT: "Intro. Disjunção 2",
        },
        needsAuxiliary: false,
    },
    disjunction_elimination: {
        label: {
            EN: "Disjunction Elim.",
            PT: "Elim. Disjunção",
        },
        needsAuxiliary: true,
        auxFormulaPlaceholder: {
            EN: "N/A",
            PT: 'Indique "A ∨ B" a eliminar:',
        },
    },
    negation_introduction: {
        label: {
            EN: "Negation Intro.",
            PT: "Intro. Negação",
        },
        needsAuxiliary: false,
    },
    negation_elimination: {
        label: {
            EN: "Negation Elim.",
            PT: "Elim. Negação",
        },
        needsAuxiliary: true,
        auxFormulaPlaceholder: {
            EN: "N/A",
            PT: 'Em "~A" a eliminar, indique A:',
        },
    },
    equivalence_introduction: {
        label: {
            EN: "Equivalence Intro.",
            PT: "Intro. Equivalência",
        },
        needsAuxiliary: false,
    },
    equivalence_elimination_1: {
        label: {
            EN: "Equivalence Elim. 1",
            PT: "Elim. Equivalência 1",
        },
        needsAuxiliary: true,
        auxFormulaPlaceholder: {
            EN: "N/A",
            PT: 'Em "A<=>B" a eliminar, indique A:',
        },
    },
    equivalence_elimination_2: {
        label: {
            EN: "Equivalence Elim. 2",
            PT: "Elim. Equivalência 2",
        },
        needsAuxiliary: true,
        auxFormulaPlaceholder: {
            EN: "N/A",
            PT: 'Em "A<=>B" a eliminar, indique B:',
        },
    },
    RAA: {
        label: {
            EN: "RAA",
            PT: "RAA",
        },
        needsAuxiliary: false
    },
    absurd_elimination: {
        label: {
            EN: "Absurd Elim.",
            PT: "Elim. Absurdo",
        },
        needsAuxiliary: false,
    },
};
