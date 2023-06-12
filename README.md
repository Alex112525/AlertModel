# Computational model of the alerting function in attention

This model is an alertness model that takes into account the circadian rhythm, memory and sound to provide a level of alertness.

The results and explanation are shown in the following link to the paper: https://www.sciencedirect.com/science/article/abs/pii/S1389041722000663

In *Main.py* you can set all the parameters like: 

* Circadian rhythm
    - In *Circadian rhythm* you can choose a list of (_start circadian rhythm, end circadian rhythm_) to set into the model that in that iteration start with that level of circadian rhythm when the sound start.
* Memory
    - In *Memory* you can choose between the _Mean (Average of past experiences)_ and _Loss memory (Forgetting memory)_ or put both in a list to use both.
* No. of samples
    - In "No. of samples" you can select the number of registers that you want to save for each module.
 
<br>

In *Model.py*, you can find the integration of all modules:

* First: We instantiate all the components, in this case, the Brain Areas, using the class in *Box.py*.

* Second: We initialize all the areas with a random value of Activation.

* Third: We connect all the areas and add the weights and their functions: *A* for _Activation_, *I* for _Inhibition_.

* Fourth: We run the model a chosen number of times (Samples).

* Fifth: We plot the behavior of the model to visualize the results.