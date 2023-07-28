# Analyseur-d-impedance-faible-a-faible-cout-pour-la-caracterisation-de-moteurs-induction
Développement d'un analyseur d'impédance à faible coût dans le but de caractériser un modèle de moteur à induction.  -  **Low cost developpement of an impedance analyzer for induction motor caracterisation. ENGLISH README comming soon.**

Tous les codes utilisés sont libre d'utilisation.

## Objectif

L'objectif de ce projet est de concevoir un outil permettant de caractériser le modèle du **moteur à induction à double cage d'écureuil** de la moto électrique ***Ambre 125*** de [Ambre](https://ambre.bike/) afin d'en prédire précisément les performances et d'en identifier les améliorations possibles. 

Le modèle standard du moteur à induction à [double cage](#comment-reconna%C3%AEtre-un-moteur-%C3%A0-double-cage) est basé sur le circuit équivalent suivant:

![plot](./Images/InkedEquivalent-circuits-for-induction-motors-a-Single-cage-b-Double-cage_W640.jpg) 

[Source de l'image](https://www.researchgate.net/publication/355849345_Influence_of_Equivalent_Circuit_Resistances_on_Operating_Parameters_on_Three-Phase_Induction_Motors_with_Powers_up_to_50_kW/figures?lo=1)

Le vrai défi réside donc dans l'identification des huits paramètres du circuit. Pormalemour y parvenir, on peut étudier l'impédance du moteur en fonction de la fréquence d'excitation. Ces données sont obtenable grâce à un [analiseur d'impédance](https://en.wikipedia.org/wiki/Impedance_analyzer#:~:text=An%20impedance%20analyzer%20is%20a,materials%20used%20to%20make%20components.). Cependant comme cet appareil est extrêmement dispendieux, une option à faible coût, avec la plage d'impédance restrainte à celle typique d'un moteur à induction, serait très utile.



## Méthode d'analyse utilisée

La méthode pour l'analyse des courbes d'impédance est décrite dans cet article[[1]](#1). Il s'agit d'étudier la réponse en fréquence au bornes de deux phases du moteur, alors que le rotor est au repos. Un algorithme d'optimisation par la méthode des moindres carrés est ensuite utilisé pour l'identification des paramètres. 

En d'autres mots, des signaux électrique sinusïdaux dont la fréquence varie entre 0 et 150 Hz, sont ainsi envoyé entre deux phases. L'amplitude doit être ajustée de façon à éviter toute saturation. Ensuite, la tension et le courant sont mesurés à haute-fréquence afin de calculer la **tension RMS**, le **courant RMS** et la **puissance moyenne**.

$` V_{RMS} = \sqrt{\frac{\sum \ _{t=0} ^N \ v(t)^2}{N}}`$

$` I_{RMS} = \sqrt{\frac{\sum \ _{t=0} ^N \ i(t)^2}{N}}`$

$` P_{moy} = \frac{\sum \ _{t=0} ^N \ i(t)\cdot v(t)}{N}`$

Ces 3 variables permettent d'obtenir les courbes de **résistances** et de **réactances** en fonction de la fréquence grâce au formules ci-dessous:

$`|Z_{eq}| = \frac{V_{RMS}}{I_{RMS}}`$

$` R_{eq} = \frac{P_{moy}}{I_{RMS}^2}`$

$` X_{eq} = \sqrt{|Z_{eq}|^2-R_{eq}^2}`$

En traçant les courbes de $` R_{eq}`$ et de $`X_{eq}`$ en fonction de la fréquence, on peut identifier les paramètres du circuit équivalent. 

## Équipement utilisé

L'appareil normalement utilisé pour produire les courbes d'impédance est un [analyseur d'impédance](https://en.wikipedia.org/wiki/Impedance_analyzer#:~:text=An%20impedance%20analyzer%20is%20a,materials%20used%20to%20make%20components.). Un tel appareil permet de balayer la fréquence de son signal de 1 à plusieurs Mhz afin d'obtenir des mesures de l'ordre de 10 µΩ à 100 TΩ. En se fiant à l'article [[1]](#1), des résultats suffisamment précis peuvent être tiré d'une analyse sur une plage de fréquence de seulement 1 à 150 Hz. Il n'est donc peut-être pas nécessaire de dépenser plusieurs millier de $ (ou €) pour un analyseur d'impédance standard.

Le dispositif qui sera mis au point devra donc remplir  ces 2 fonctions:

### Produire un signal électrique sinusoïdale à fréquence variable

D'abord, un signal électrique, en tension ou en courant, doit pouvoir être appliquée aux bornes de deux phases du moteur. Ce signal doit idéalement n'être que sinusoïdale avec un contenu fréquentiel ne contenant que la fréquence désirée. La puissance du signal doit aussi être suffisante pour que la tension et le courant soit précisément mesurables.

Un générateur de fonction ainsi qu'un amplificateur approprié peuvent donc être employés pour remplir cette tâche. Cependant ces appareils sont aussi relativement dispendieux et une option à très faible coût méritait d'être tentée: l'amplificateur hi-fi.

Un tel amplificateur, destiné au contrôle de haut-parleurs, devrait pouvoir générer un signal arbitraire dont la fréquence n'excède pas 20 kHz. De plus, ces appareils sont très peu couteux et peuvent fournir une puissance appréciable. On choisi donc l'amplificateur hi-fi ZK-1002M capable de générer 100W ce qui devrait être suffisant.

<img src="./Images/zk-1002m.jpg" alt="drawing" style="width:200px;"/>  <img src="./Images/R5-100W.jpg" alt="drawing" style="width:200px;"/>

Comme il est conçu pour contrôler un haut-parleur dont l'impédance de 4 à 8 Ohm, une résistance de puissance (100W pour être certain...) sera mise en série avec les phase du moteur. Cette même résistance servira d'ailleurs à mesurer le courant.

### Mesurer simultannément de la tension et du courant à haute fréquence

Traditionnelement, les mesures à effectuer nécessiterait un générateur de fonction, un amplificateur (pour amplifier le signal) et un oscilloscope (ou la combinaison wattmètre + ampèremètre + voltmètre assez précis). Il va sans dire que ces équipements sont dispendieux. 

Pour remplacer le générateur de fonction et l'amplificateur, l'amplificateur audio HiFi ZK-1002M (100W), normalement destiné au contrôle d'haut-parleurs. Une résistance de puissance de 5 Ohm (100W) est mis en série avec les phases du moteur afin de simuler l'impédance d'un haut-parleur.

Ensuite, un micro-contrôlleur ESP-32, ainsi qu'un circuit d'amplificateurs opérationnels, sont utilisés pour prendre les mesures nécessaires.

  <img src="./Images/esp32.jpg" alt="drawing" style="width:200px;"/>

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


#### Comment reconnaître un moteur à double cage?

Dans les documents de références du moteur, on remarque que la courbe de couple est similaire à celle-ci:

![plot](./Images/Torque-speed-curves-II-EQUVIVALENT-CIRCUIT-DIAGRAM-AND-ITS-SOLUTION_W640.jpg) 

[Source de l'image](https://www.researchgate.net/publication/318692438_Influence_of_rotor_slot_shape_on_the_parameters_of_induction_motor/figures?lo=1)

Le comportement du moteur n'est donc pas explicable avec le modèle à une seule cage.


## References
<a id="1">[1]</a> 
Monjo, Lluis, Kojooyan-Jafari, Hengameh, Corcoles, Felipe and
Pedra, Joaquim (2015) Squirrel-cage induction motor parameter
estimation using a variable frequency test. IEEE Transactions on
Energy Conversion, 30. 550-557. Doi: 10.1109/TEC.2014.2362964
