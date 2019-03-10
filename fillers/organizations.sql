SELECT Nom.NOM_ASSUJ, Entreprise.*
  FROM Entreprise
         LEFT JOIN Nom ON Entreprise.NEQ = Nom.[NEQ]
  WHERE
        Entreprise.COD_FORME_JURI = 'APE'
    AND Entreprise.COD_ACT_ECON_CAE = 8621
    AND (Entreprise.ADR_DOMCL_LIGN2_ADR LIKE '%Montréal (Québec)%' OR Entreprise.ADR_DOMCL_LIGN2_ADR LIKE '%Québec (Québec)%')
    AND NOM_LOCLT_CONSTI LIKE 'Québec'