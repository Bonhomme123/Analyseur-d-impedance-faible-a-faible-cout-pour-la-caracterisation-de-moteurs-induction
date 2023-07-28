# Identification-des-parametres-du-moteur-induction-avec-ESP32
Méthode à faible coût pour identifier les paramètres du circuit d'un moteur à induction.  -  Low cost method for parameters identifications of induction motor's equivalent circuit.

## Objectif

L'objectif de ce projet est de modéliser le **moteur à induction à double cages d'écureuil** de la moto électrique ***Ambre 125*** de [Ambre](https://ambre.bike/) afin d'en prédire précisément les performances et d'en identifier les améliorations possibles.

Le modèle standard du moteur à induction à cages doubles est basé sur le circuit équivalent suivant:

![plot](./Images/InkedEquivalent-circuits-for-induction-motors-a-Single-cage-b-Double-cage_W640.jpg) 

[Source de l'image](https://www.researchgate.net/publication/355849345_Influence_of_Equivalent_Circuit_Resistances_on_Operating_Parameters_on_Three-Phase_Induction_Motors_with_Powers_up_to_50_kW/figures?lo=1)

Le vrai défi réside donc dans l'identification des huits paramètres du circuit.


#### Comment reconnaître un moteur à cage double?

Dans les documents de références du moteur, on remarque que la courbe de couple est similaire à celle-ci:

![plot](./Images/Torque-speed-curves-II-EQUVIVALENT-CIRCUIT-DIAGRAM-AND-ITS-SOLUTION_W640.jpg) 

[Source de l'image](https://www.researchgate.net/publication/318692438_Influence_of_rotor_slot_shape_on_the_parameters_of_induction_motor/figures?lo=1)

Le comportement du moteur n'est donc pas explicable avec le modèle à une seule cage.

### Méthode utilisée

La méthode employée est décrite dans cet article[[1]](#1). Il s'agit d'étudier la réponse en fréquence au bornes de deux phases du moteur, alors que le rotor est au repos. Un algorithme d'optimisation par la méthode des moindres carrés est ensuite utilisé pour l'identification des paramètres. 

En d'autres mots, des signaux électrique sinusïdaux dont la fréquence varie entre 0 et 150 Hz, sont ainsi envoyé entre deux phases. L'amplitude doit être ajustée de façon à éviter toute saturation. Ensuite, la tension et le courant sont mesurés à haute-fréquence afin de calculer la **tension RMS**, le **courant RMS** et la **puissance moyenne**.

$` V_{RMS} = \sqrt{\frac{\sum \ _{t=0} ^N \ v(t)^2}{N}}`$

$` I_{RMS} = \sqrt{\frac{\sum \ _{t=0} ^N \ i(t)^2}{N}}`$

$` P_{moy} = \frac{\sum \ _{t=0} ^N \ i(t)\cdot v(t)}{N}`$

Ces 3 variables permettent d'obtenir les courbes de **résistances** et de **réactances** en fonction de la fréquence grâce au formules ci-dessous:

$`|Z_{eq}| = \frac{V_{RMS}}{I_{RMS}}`$

$` R_{eq} = \frac{P_{moy}}{I_{RMS}^2}`$

$` X_{eq} = \sqrt{|Z_{eq}|^2-R_{eq}^2}`$

En traçant les courbes de $` R_{eq}`$ et de $`X_{eq}`$ en fonction de la fréquence, on peut identifier les paramètres du circuit équivalent. 

### Équipement utilisé

Traditionnelement, les mesures à effectuer nécessiterait un générateur de fonction, un amplificateur (pour amplifier le signal) et un oscilloscope (ou la combinaison wattmètre + ampèremètre + voltmètre assez précis). Il va sans dire que ces équipements sont dispendieux. 

Pour remplacer le générateur de fonction et l'amplificateur, l'amplificateur audio HiFi ZK-1002M (100W), normalement destiné au contrôle d'haut-parleurs. Une résistance de puissance de 5 Ohm (100W) est mis en série avec les phases du moteur afin de simuler l'impédance d'un haut-parleur.

Ensuite, un micro-contrôlleur ESP-32, ainsi qu'un circuit d'amplificateurs opérationnels, sont utilisés pour prendre les mesures nécessaires.

<img src="./Images/zk-1002m.jpg" alt="drawing" style="width:200px;"/> <img src="./Images/R5-100W.jpg" alt="drawing" style="width:200px;"/> <img src="./Images/esp32.jpg" alt="drawing" style="width:200px;"/>

## Circuit
Le circuit est disponible [ici](https://github.com/Bonhomme123/Identification-des-parametres-du-moteur-induction-avec-ESP32/tree/main/SSFR%20Induction%20motor%20circuit) et est visualisable avec KiCad.

<img src="./Images/SSFR Induction motor — Editeur de Schématique 2023-07-25 17_00_29 (2).png" alt="drawing" style="width:800px;"/>

### Nécessité d'un filtre passe-bas
à venir

### Ampli. de mesures

à venir

### Réference de tension 



## Mesures
 À venir...
  (code esp32, protocole, callibration etc.)
## Analyse
### Hypothèse
* résistance de puissance purement résistive
* mesure simultannée?
  
à venir... (code python, incertitude)
## Résultats
À venir...

## Amélioration possible
* Utiliser un vrai amplificateur de mesure (INA118, INA128, etc.)
* Contrôle du courant automatique (contrôle du volume audio...)

## References
<a id="1">[1]</a> 
Monjo, Lluis, Kojooyan-Jafari, Hengameh, Corcoles, Felipe and
Pedra, Joaquim (2015) Squirrel-cage induction motor parameter
estimation using a variable frequency test. IEEE Transactions on
Energy Conversion, 30. 550-557. Doi: 10.1109/TEC.2014.2362964
