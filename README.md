# Identification-des-parametres-du-moteur-induction-avec-ESP32
Méthode à faible coût pour identifier les paramètres du circuit d'un moteur à induction.  -  Low cost method for parameters identifications of induction motor's equivalent circuit.
## Objectif

L'objectif de ce projet est de mesurer la réponse en fréquence d'un moteur à induction à double cage d'écureuil, au repos, afin d'en identifier les paramètres du circuits équivalent. Ce circuit est le suivant:

![plot](./Images/InkedEquivalent-circuits-for-induction-motors-a-Single-cage-b-Double-cage_W640.jpg) 

[Source de l'image](https://www.researchgate.net/publication/355849345_Influence_of_Equivalent_Circuit_Resistances_on_Operating_Parameters_on_Three-Phase_Induction_Motors_with_Powers_up_to_50_kW/figures?lo=1)


### Comment reconnaître un moteur à cage double?

Dans les documents de références du moteur, on remarque que la courbe de couple est similaire à celle-ci:

![Alt text](https://www.researchgate.net/profile/Petr-Kacor/publication/318692438/figure/fig3/AS:711059639898113@1546541237549/Torque-speed-curves-II-EQUVIVALENT-CIRCUIT-DIAGRAM-AND-ITS-SOLUTION_W640.jpg)
