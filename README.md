# Identification-des-parametres-du-moteur-induction-avec-ESP32
Méthode à faible coût pour identifier les paramètres du circuit d'un moteur à induction.  -  Low cost method for parameters identifications of induction motor's equivalent circuit.
## Objectif

L'objectif de ce projet est de mesurer la réponse en fréquence d'un moteur à induction à double cage d'écureuil, au repos, afin d'en identifier les paramètres du circuits équivalent. Ce circuit est le suivant:

![plot](./Images/InkedEquivalent-circuits-for-induction-motors-a-Single-cage-b-Double-cage_W640.jpg) 

[Source de l'image](https://www.researchgate.net/publication/355849345_Influence_of_Equivalent_Circuit_Resistances_on_Operating_Parameters_on_Three-Phase_Induction_Motors_with_Powers_up_to_50_kW/figures?lo=1)


### Comment reconnaître un moteur à cage double?

Dans les documents de références du moteur, on remarque que la courbe de couple est similaire à celle-ci:

![plot](./Images/Torque-speed-curves-II-EQUVIVALENT-CIRCUIT-DIAGRAM-AND-ITS-SOLUTION_W640.jpg) 

[Source de l'image](https://www.researchgate.net/publication/318692438_Influence_of_rotor_slot_shape_on_the_parameters_of_induction_motor/figures?lo=1)

Le comportement du moteur n'est donc pas explicable avec le modèle à une seule cage.

### Équipement utilisé

Traditionnelement, les mesures à effectuer nécessiterait un générateur de fonction, un amplificateur (pour amplifier le signal) et un oscilloscope (ou la combinaison wattmètre + ampèremètre + voltmètre assez précis). Il va sans dire que ces équipements sont dispendieux. 

Pour remplacer le générateur de fonction et l'amplificateur, l'amplificateur audio HiFi ZK-1002M (100W), normalement destiné au contrôle d'haut-parleurs.

### Méthode utilisée

La méthode employée est décrite dans cet article[[1]](#1). Il s'agit d'étudier la réponse en fréquence au bornes de deux phases du moteur, alors que le rotor est au repos. Un algorithme d'optimisation par la méthode des moindres carrés est ensuite utilisé pour l'identification des paramètres. 


## Mesures

Afin de mesurer 

## Circuit




## Résultats

À venir...

## References
<a id="1">[1]</a> 
Monjo, Lluis, Kojooyan-Jafari, Hengameh, Corcoles, Felipe and
Pedra, Joaquim (2015) Squirrel-cage induction motor parameter
estimation using a variable frequency test. IEEE Transactions on
Energy Conversion, 30. 550-557. Doi: 10.1109/TEC.2014.2362964
