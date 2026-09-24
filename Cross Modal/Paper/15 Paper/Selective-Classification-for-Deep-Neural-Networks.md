# **Selective Classification for Deep Neural Networks**

**Yonatan Geifman**
Computer Science Department
Technion – Israel Institute of Technology
```
 yonatan.g@cs.technion.ac.il

```

**Ran El-Yaniv**
Computer Science Department
Technion – Israel Institute of Technology
```
  rani@cs.technion.ac.il

```

**Abstract**

Selective classification techniques (also known as reject option) have not yet been considered in the context of deep neural networks (DNNs). These techniques can potentially significantly improve DNNs prediction performance by trading-off coverage. In this paper we propose a method to construct a selective classifier given a trained neural network. Our method allows a user to set a desired risk level. At test time, the classifier rejects instances as needed, to grant the desired risk (with high probability). Empirical results over CIFAR and ImageNet convincingly demonstrate the viability of our method, which opens up possibilities to operate DNNs in mission-critical applications. For example, using our method an unprecedented 2% error in top-5 ImageNet classification can be guaranteed with probability 99.9%, and almost 60% test coverage.

**1** **Introduction**

While self-awareness remains an illusive, hard to define concept, a rudimentary kind of self-awareness, which is much easier to grasp, is the ability to know what you don’t know, which can make you smarter. The subfield dealing with such capabilities in machine learning is called _selective prediction_
(also known as prediction with a _reject option_ ), which has been around for 60 years [1, 5]. The main motivation for selective prediction is to reduce the error rate by abstaining from prediction when in doubt, while keeping coverage as high as possible. An ultimate manifestation of selective prediction is a classifier equipped with a “dial” that allows for precise control of the desired true error rate
(which should be guaranteed with high probability), while keeping the coverage of the classifier as high as possible.

Many present and future tasks performed by (deep) predictive models can be dramatically enhanced by high quality selective prediction. Consider, for example, autonomous driving. Since we cannot rely on the advent of “singularity”, where AI is superhuman, we must manage with standard machine learning, which sometimes errs. But what if our deep autonomous driving network were capable of knowing that it doesn’t know how to respond in a certain situation, disengaging itself in advance and alerting the human driver (hopefully not sleeping at that time) to take over? There are plenty of other mission-critical applications that would likewise greatly benefit from effective selective prediction.

The literature on the reject option is quite extensive and mainly discusses rejection mechanisms for various hypothesis classes and learning algorithms, such as SVM, boosting, and nearest-neighbors

[8, 13, 3]. The reject option has rarely been discussed in the context of neural networks (NNs), and so far has not been considered for deep NNs (DNNs). Existing NN works consider a cost-based rejection model [2, 4], whereby the costs of misclassification and abstaining must be specified, and a rejection mechanism is optimized for these costs. The proposed mechanism for classification is based on applying a carefully selected threshold on the maximal neuronal response of the softmax layer.
We that call this mechanism _softmax response_ (SR). The cost model can be very useful when we can quantify the involved costs, but in many applications of interest meaningful costs are hard to reason.
(Imagine trying to set up appropriate rejection/misclassification costs for disengaging an autopilot

31st Conference on Neural Information Processing Systems (NIPS 2017), Long Beach, CA, USA.

driving system.) Here we consider the alternative risk-coverage view for selective classification discussed in [5].

Ensemble techniques have been considered for selective (and confidence-rated) prediction, where rejection mechanisms are typically based on the ensemble statistics [18, 7]. However, such techniques are presently hard to realize in the context of DNNs, for which it could be very costly to train sufficiently many ensemble members. Recently, Gal and Ghahramani [9] proposed an ensemble-like method for measuring uncertainty in DNNs, which bypasses the need to train several ensemble members. Their method works via sampling multiple dropout applications of the forward pass to perturb the network prediction randomly. While this Monte-Carlo dropout (MC-dropout) technique was not mentioned in the context of selective prediction, it can be directly applied as a viable selective prediction method using a threshold, as we discuss here.

In this paper we consider classification tasks, and our goal is to learn a selective classifier ( _f, g_ ), where _f_ is a standard classifier and _g_ is a rejection function. The selective classifier has to allow full _guaranteed_ control over the true risk. The ideal method should be able to classify samples in production with any desired level of risk with the _optimal_ coverage rate. It is reasonable to assume that this optimal performance can only be obtained if the pair ( _f, g_ ) is trained together. As a first step, however, we consider a simpler setting where a (deep) neural classifier _f_ is already given, and our goal is to learn a rejection function _g_ that will guarantee with high probability a desired error rate.
To this end, we consider the above two known techniques for rejection (SR and MC-dropout), and devise a learning method that chooses an appropriate threshold that ensures the desired risk. For a given classifier _f_, confidence level _δ_, and desired risk _r_ _[∗]_, our method outputs a selective classifier
( _f, g_ ) whose test error will be no larger than _r_ _[∗]_ with probability of at least 1 _−_ _δ_ .

Using the well-known VGG-16 architecture, we apply our method on CIFAR-10, CIFAR-100 and
ImageNet (on ImageNet we also apply the RESNET-50 architecture). We show that both SR and dropout lead to extremely effective selective classification. On both the CIFAR datasets, these two mechanisms achieve nearly identical results. However, on ImageNet, the simpler SR mechanism is significantly superior. More importantly, we show that almost any desirable risk level can be guaranteed with a surprisingly high coverage. For example, an unprecedented 2% error in top-5
ImageNet classification can be guaranteed with probability 99.9%, and almost 60% test coverage.

**2** **Problem Setting**

We consider a standard multi-class classification problem. Let _X_ be some feature space (e.g., raw image data) and _Y_, a finite label set, _Y_ = _{_ 1 _,_ 2 _,_ 3 _, . . ., k}_, representing _k_ classes. Let _P_ ( _X, Y_ ) be a distribution over _X_ _× Y_ . A classifier _f_ is a function _f_ : _X_ _→Y_, and the _true risk_ of _f_ w.r.t. _P_ is _R_ ( _f_ _|P_ ) =∆ _EP_ ( _X,Y_ )[ _ℓ_ ( _f_ ( _x_ ) _, y_ )], where _ℓ_ : _Y_ _× Y_ _→_ R+ is a given loss function, for example the 0/1 error. Given a labeled set _Sm_ = _{_ ( _xi, yi_ ) _}_ _[m]_ _i_ =1 _[⊆]_ [(] _[X]_ _[× Y]_ [)][ sampled i.i.d.] [from] _[ P]_ [(] _[X, Y]_ [ )][, the]

the 0/1 error. Given a labeled set _Sm_ = _{_ ( _xi, yi_ ) _}_ _[m]_ _i_ =1 _[⊆]_ [(] _[X]_ _[× Y]_ [)][ sampled i.i.d.] [from] _[ P]_ [(] _[X, Y]_ [ )][, the]

_empirical risk_ of the classifier _f_ is ˆ _r_ ( _f_ _|Sm_ ) =∆ _m_ 1 - _mi_ =1 _[ℓ]_ [(] _[f]_ [(] _[x][i]_ [)] _[, y][i]_ [)][.]

A _selective classifier_ [5] is a pair ( _f, g_ ), where _f_ is a classifier, and _g_ : _X_ _→{_ 0 _,_ 1 _}_ is a _selection_
_function_, which serves as a binary qualifier for _f_ as follows,

- _m_
_i_ =1 _[ℓ]_ [(] _[f]_ [(] _[x][i]_ [)] _[, y][i]_ [)][.]

( _f, g_ )( _x_ ) =∆

- _f_ ( _x_ ) _,_ if _g_ ( _x_ ) = 1;
don’t know _,_ if _g_ ( _x_ ) = 0.

Thus, the selective classifier abstains from prediction at a point _x_ iff _g_ ( _x_ ) = 0. The performance of a selective classifier is quantified using _coverage_ and _risk_ . Fixing _P_, coverage, defined to be
_φ_ ( _f, g_ ) =∆ _EP_ [ _g_ ( _x_ )] _,_ is the probability mass of the non-rejected region in _X_ . The selective risk of
( _f, g_ ) is

∆ _[E]_ _P_ [[] _[ℓ]_ [(] _[f]_ [(] _[x]_ [)] _[, y]_ [)] _[g]_ [(] _[x]_ [)]]
_R_ ( _f, g_ ) = _._ (1)

_φ_ ( _f, g_ )

Clearly, the risk of a selective classifier can be traded-off for coverage. The entire performance profile of such a classifier can be specified by its _risk-coverage_ curve, defined to be risk as a function of coverage [5].

Consider the following problem. We are given a classifier _f_, a training sample _Sm_, a _confidence_ parameter _δ_ _>_ 0, and a desired _risk target r_ _[∗]_ _>_ 0. Our goal is to use _Sm_ to create a selection function

2

_g_ such that the selective risk of ( _f, g_ ) satisfies

**Pr** _Sm {R_ ( _f, g_ ) _> r_ _[∗]_ _} < δ,_ (2)

where the probability is over training samples, _Sm_, sampled i.i.d. from the unknown underlying distribution _P_ . Among all classifiers satisfying (2), the best ones are those that maximize the coverage.
For a fixed _f_, and a given class _G_ (which will be discussed below), in this paper our goal is to select
_g_ _∈G_ such that the selective risk _R_ ( _f, g_ ) satisfies (2) while the coverage Φ( _f, g_ ). is maximized.

**3** **Selection with Guaranteed Risk Control**

In this section, we present a general technique for constructing a selection function with guaranteed performance, based on a given classifier _f_, and a confidence-rate function _κf_ : _X_ _→_ R [+] for _f_ .
We do not assume anything on _κf_, and the _interpretation_ is that _κ_ can rank in the sense that if
_κf_ ( _x_ 1) _≥_ _κf_ ( _x_ 2), for _x_ 1 _, x_ 2 _∈X_, the confidence function _κf_ indicates that the confidence in the prediction _f_ ( _x_ 2) is not higher than the confidence in the prediction _f_ ( _x_ 1). In this section we are not concerned with the question of what is a good _κf_ (which is discussed in Section 4); our goal is to generate a selection function _g_, with guaranteed performance for a given _κf_ .

For the reminder of this paper, the loss function _ℓ_ is taken to be the standard 0/1 loss function (unless explicitly mentioned otherwise). Let _Sm_ = _{_ ( _xi, yi_ ) _}_ _[m]_ _i_ =1 _[⊆]_ [(] _[X]_ _[× Y]_ [)] _[m]_ [be a training set, assumed]

to be sampled i.i.d. from an unknown distribution _P_ ( _X, Y_ ). Given also are a _confidence_ parameter
_δ_ _>_ 0, and a desired _risk target r_ _[∗]_ _>_ 0. Based on _Sm_, our goal is to learn a selection function _g_ such that the selective risk of the classifier ( _f, g_ ) satisfies (2).

For _θ_ _>_ 0, we define the selection function _gθ_ : _X_ _→{_ 0 _,_ 1 _}_ as

_gθ_ ( _x_ ) = _gθ_ ( _x|κf_ ) =∆

- 1 _,_ if _κf_ ( _x_ ) _≥_ _θ_ ; (3)
0 _,_ otherwise.

For any selective classifier ( _f, g_ ), we define its _empirical selective risk_ with respect to the labeled sample _Sm_,

_,_

- _m_
_i_ =1 _[ℓ]_ [(] _[f]_ [(] _[x][i]_ [)] _[, y][i]_ [)] _[g]_ [(] _[x][i]_ [)]

_r_ ˆ( _f, g|Sm_ ) =∆

1
_m_

_φ_ ˆ( _f, g|Sm_ )

where _φ_ [ˆ] is the _empirical_ _coverage_, _φ_ [ˆ] ( _f, g|Sm_ ) =∆ _m_ 1 - _mi_ =1 _[g]_ [(] _[x][i]_ [)][.] [For] [any] [selection] [function] _[g]_ [,]

denote by _g_ ( _Sm_ ) the _g_ -projection of _Sm_, _g_ ( _Sm_ ) =∆ _{_ ( _x, y_ ) _∈_ _Sm_ : _g_ ( _x_ ) = 1 _}_ .

The _selection with guaranteed risk_ (SGR) learning algorithm appears in Algorithm 1. The algorithm receives as input a classifier _f_, a confidence-rate function _κf_, a confidence parameter _δ_ _>_ 0, a target risk _r_ _[∗]_ [1], and a training set _Sm_ . The algorithm performs a binary search to find the optimal bound guaranteeing the required risk with sufficient confidence. The SGR algorithm outputs a selective classifier ( _f, g_ ) and a risk bound _b_ _[∗]_ . In the rest of this section we analyze the SGR algorithm. We make use of the following lemma, which gives the tightest possible numerical generalization bound for a single classifier, based on a test over a labeled sample.

**Lemma 3.1 (Gascuel and Caraux, 1992, [10])** _Let P_ _be any distribution and consider a classifier_
_f_ _whose true error w.r.t._ _P_ _is R_ ( _f_ _|P_ ) _._ _Let_ 0 _<_ _δ_ _<_ 1 _be given and let_ _r_ ˆ( _f_ _|Sm_ ) _be the empirical_
_error of f_ _w.r.t._ _to the labeled set Sm, sampled i.i.d._ _from P_ _._ _Let B_ _[∗]_ (ˆ _ri, δ, Sm_ ) _be the solution b of_
_the following equation,_

_m·r_ ˆ( _f_ _|Sm_ )

_j_ =0

- _m_
_b_ _[j]_ (1 _−_ _b_ ) _[m][−][j]_ = _δ._ (4)

_j_

_Then,_ **Pr** _Sm{R_ ( _f_ _|P_ ) _> B_ _[∗]_ (ˆ _ri, δ, Sm_ ) _} < δ._

We emphasize that the numerical bound of Lemma 3.1 is the tightest possible in this setting. As discussed in [10], the analytic bounds derived using, e.g., Hoeffding inequality (or other concentration inequalities), approximate this numerical bound and incur some slack.

1Whenever the triplet _Sm_, _δ_ and _r∗_ is infeasible, the algorithm will return a vacuous solution with zero coverage.

3

**Algorithm 1** _Selection with Guaranteed Risk_ (SGR)

1: SGR( _f_, _κf_, _δ_, _r_ _[∗]_, _Sm_ )
2: Sort _Sm_ according to _κf_ ( _xi_ ), _xi_ _∈_ _Sm_ (and now assume w.l.o.g. that indices reflect this ordering).
3: _z_ min = 1; _z_ max = _m_
4: **for** _i_ = 1 **to** _k_ =∆ _⌈_ log2 _m⌉_ **do**
5: _z_ = _⌈_ ( _z_ min + _z_ max) _/_ 2 _⌉_
6: _θ_ = _κf_ ( _xz_ )
7: _gi_ = _gθ_ {(see (3))}
8: _r_ ˆ _i_ = _r_ ˆ( _f, gi|Sm_ )
9: _b_ _[∗]_ [=] _[ B][∗]_ [(ˆ] _[r][i][, δ/][⌈]_ [log] _[m][⌉][, g][i]_ [(] _[S][m]_ [))][ {see Lemma 3.1 }]

9: _b_ _[∗]_ _i_ [=] _[ B][∗]_ [(ˆ] _[r][i][, δ/][⌈]_ [log] 2 _[m][⌉][, g][i]_ [(] _[S][m]_ [))][ {see Lemma 3.1 }]

10: **if** _b_ _[∗]_ _[< r][∗]_ **[then]**

10: **if** _b_ _[∗]_ _i_ _[< r][∗]_ **[then]**

11: _z_ max = _z_
12: **else**
13: _z_ min = _z_
14: **end if**
15: **end for**
16: Output- ( _f, gk_ ) and the bound _b_ _[∗]_ _k_ [.]

For any selection function, _g_, let _Pg_ ( _X, Y_ ) be the projection of _P_ over _g_ ; that is, _Pg_ ( _X, Y_ ) =∆

_P_ ( _X, Y |g_ ( _X_ ) = 1). The following theorem is a uniform convergence result for the SGR procedure.

**Theorem 3.2 (SGR)** _Let Sm_ _be a given labeled set, sampled i.i.d._ _from P_ _, and consider an appli-_
_cation of the SGR procedure._ _For k_ =∆ _⌈_ log2 _m⌉, let_ ( _f, gi_ ) _and b∗i_ _[,][ i]_ [=] [1] _[, . . ., k][, be the selective]_

_classifier and bound computed by SGR in its ith iterations._ _Then,_

**Pr** _Sm {∃i_ : _R_ ( _f_ _|Pgi_ ) _> B_ _[∗]_ (ˆ _ri, δ/k, gi_ ( _Sm_ )) _} < δ._

**Proof Sketch:** For any _i_ = 1 _, . . ., k_, let _mi_ = _|gi_ ( _Sm_ ) _|_ be the random variable giving the size of accepted examples from _Sm_ on the _i_ th iteration of SGR. For any fixed value of 0 _≤_ _mi_ _≤_ _m_, by
Lemma 3.1, applied with the projected distribution _Pgi_ ( _X, Y_ ), and a sample _Smi_, consisting of _mi_ examples drawn from the product distribution ( _Pgi_ ) _[m][i]_,

**Pr** _Smi_ _∼_ ( _Pgi_ ) _[m]_ _i_ _{R_ ( _f_ _|Pgi_ ) _> B_ _[∗]_ (ˆ _ri, δ/k, gi_ ( _Sm_ )) _} < δ/k._ (5)

The sampling distribution of _mi_ labeled examples in SGR is determined by the following process:
sample a set _Sm_ of _m_ examples from the product distribution _P_ _[m]_ and then use _gi_ to filter _Sm_, resulting in a (randon) number _mi_ of examples. Therefore, the left-hand side of (5) equals

**Pr** _Sm∼P_ _[m]_ _{R_ ( _f_ _|Pgi_ ) _> B_ _[∗]_ (ˆ _ri, δ/k, gi_ ( _Sm_ )) _|gi_ ( _Sm_ ) = _mi} ._

Clearly,

Therefore,

=

_R_ ( _f_ _|Pgi_ ) = _EPgi_ [ _ℓ_ ( _f_ ( _x_ ) _, y_ )] = _[E][P]_ [ [] _[ℓ]_ [(] _[f]_ _φ_ [(] ( _[x]_ _f, g_ [)] _[, y]_ ) [)] _[g]_ [(] _[x]_ [)]] = _R_ ( _f, gi_ ) _._

**Pr** _Sm{R_ ( _f, gi_ ) _> B_ _[∗]_ (ˆ _ri, δ/k, gi_ ( _Sm_ )) _}_

_m_

_n_ =0

**Pr** _Sm_ _{R_ ( _f, gi_ ) _> B_ _[∗]_ (ˆ _ri, δ/k, gi_ ( _Sm_ )) _| gi_ ( _Sm_ ) = _n} ·_ **Pr** _{gi_ ( _Sm_ ) = _n}_

_δ_
_≤_
_k_

_m_

_n_ =0

**Pr** _{gi_ ( _Sm_ ) = _n}_ = _[δ]_

_k_ _[.]_

An application of the union bound completes the proof.

**4** **Confidence-Rate Functions for Neural Networks**

Consider a classifier _f_, assumed to be trained for some unknown distribution _P_ . In this section we consider two confidence-rate functions, _κf_, based on previous work [9, 2]. We note that an ideal

4

confidence-rate function _κf_ ( _x_ ) for _f_, should reflect true loss monotonicity. Given ( _x_ 1 _, y_ 1) _∼_ _P_ and
( _x_ 2 _, y_ 2) _∼_ _P_, we would like the following to hold: _κf_ ( _x_ 1) _≤_ _κf_ ( _x_ 2) if and only if _ℓ_ ( _f_ ( _x_ 1) _, y_ 1) _≥_

_ℓ_ ( _f_ ( _x_ 2) _, y_ 2). Obviously, one cannot expect to have an ideal _κf_ . Given a confidence-rate functions
_κf_, a useful way to analyze its effectiveness is to draw the risk-coverage curve of its induced rejection function, _gθ_ ( _x|κf_ ), as defined in (3). This risk-coverage curve shows the relationship between _θ_ and _R_ ( _f, gθ_ ). For example, see Figure 2(a) where a two (nearly identical) risk-coverage curves are plotted. While the confidence-rate functions we consider are not ideal, they will be shown empirically to be extremely effective. [2]

The first confidence-rate function we consider has been around in the NN folklore for years, and is explicitly mentioned by [2, 4] in the context of reject option. This function works as follows: given any neural network classifier _f_ ( _x_ ) where the last layer is a softmax, we denote by _f_ ( _x|j_ ) the soft response output for the _j_ th class. The confidence-rate function is defined as _κ_ =∆ max _j∈Y_ ( _f_ ( _x|j_ )).
We call this function _softmax response_ (SR).

Softmax responses are often treated as probabilities (responses are positive and sum to 1), but some authors criticize this approach [9]. Noting that, for our purposes, the ideal confidence-rate function should only provide coherent _ranking_ rather than absolute probability values, softmax responses are potentially good candidates for _relative_ confidence rates.

We are not familiar with a rigorous explanation for SR, but it can be intuitively motivated by observing neuron activations. For example, Figure 1 depicts average response values of every neuron in the second-to-last layer for true positives and false positives for the class ‘8’ in the MNIST dataset (and qualitatively similar behavior occurs in all MNIST classes). The x-axis corresponds to neuron indices in that layer (1-128); and the y-axis shows the average responses, where green squares are averages of true positives, boldface squares highlight strong responses, and red circles correspond to the average response of false positives. It is evident that the true positive activation response in the active neurons is much higher than the false positive, which is expected to be reflected in the final softmax layer response. Moreover, it can be seen that the large activation values are spread over many neurons, indicating that the confidence signal arises due to numerous patterns detected by neurons in this layer.
Qualitatively similar behavior can be observed in deeper layers.

Figure 1: Average response values of neuron activations for class "8" on the MNIST dataset; green squares, true positives, red circles, false negatives

The MC-dropout technique we consider was recently proposed to quantify uncertainty in neural networks [9]. To estimate uncertainty for a given instance _x_, we run a number of feed-forward iterations over _x_, each applied with dropout in the last fully connected layer. Uncertainty is taken as the variance in the responses of the neuron corresponding to the most probable class. We consider minus uncertainty as the MC-dropout confidence rate.

**5** **Empirical Results**

In Section 4 we introduced the SR and MC-dropout confidence-rate function, defined for a given model _f_ . We trained VGG models [17] for CIFAR-10, CIFAR-100 and ImageNet. For each of these models _f_, we considered both the SR and MC-dropout confidence-rate functions, _κf_, and the induced

2While Theorem 3.2 always holds, we note that if _κf_ is severely skewed (far from ideal), the bound of the resulting selective classifier can be far from the target risk.

5

rejection function, _gθ_ ( _x|κf_ ). In Figure 2 we present the risk-coverage curves obtained for each of the three datasets. These curves were obtained by computing a validation risk and coverage for many _θ_ values. It is evident that the risk-coverage profile for SR and MC-dropout is nearly identical for both the CIFAR datasets. For the ImageNet set we plot the curves corresponding to top-1 (dashed curves) and top-5 tasks (solid curves). On this dataset, we see that SR is significantly better than MC-dropout on both tasks. For example, in the top-1 task and 60% coverage, the SR rejection has 10% error while
MC-dropout rejection incurs more than 20% error. But most importantly, these risk-coverage curves show that selective classification can potentially be used to dramatically reduce the error in the three datasets. Due to the relative advantage of SR, in the rest of our experiments we only focus on the SR rating.

(a) CIFAR-10 (b) CIFAR-100 (c) Image-Net

Figure 2: Risk coverage curves for (a) cifar-10, (b) cifar-100 and (c) image-net (top-1 task: dashed curves; top-5 task: solid crves), SR method in blue and MC-dropout in red.

We now report on experiments with our SGR routine, and apply it on each of the datasets to construct high probability risk-controlled selective classifiers for the three datasets.

Table 1: Risk control results for CIFAR-10 for _δ_ = 0 _._ 001

Desired risk ( _r_ _[∗]_ ) Train risk Train coverage Test risk Test coverage Risk bound ( _b_ _[∗]_ )

0.01 0.0079 0.7822 0.0092 0.7856 0.0099
0.02 0.0160 0.8482 0.0149 0.8466 0.0199
0.03 0.0260 0.8988 0.0261 0.8966 0.0298
0.04 0.0362 0.9348 0.0380 0.9318 0.0399
0.05 0.0454 0.9610 0.0486 0.9596 0.0491
0.06 0.0526 0.9778 0.0572 0.9784 0.0600

**5.1** **Selective Guaranteed Risk for CIFAR-10**

We now consider CIFAR-10; see [14] for details. We used the VGG-16 architecture [17] and adapted it to the CIFAR-10 dataset by adding massive dropout, exactly as described in [15]. We used data augmentation containing horizontal flips, vertical and horizontal shifts, and rotations, and trained using SGD with momentum of 0.9, initial learning rate of 0.1, and weight decay of 0.0005. We multiplicatively dropped the learning rate by 0.5 every 25 epochs, and trained for 250 epochs. With this setting we reached validation accuracy of 93.54, and used the resulting network _f_ 10 as the basis for our selective classifier.

We applied the SGR algorithm on _f_ 10 with the SR confidence-rating function, where the training set for SGR, _Sm_, was taken as half of the standard CIFAR-10 validation set that was randomly split to two equal parts. The other half, which was not consumed by SGR for training, was reserved for testing the resulting bounds. Thus, this training and test sets where each of approximately 5000 samples. We applied the SGR routine with several desired risk values, _r_ _[∗]_, and obtained, for each such _r_ _[∗]_, corresponding selective classifier and risk bound _b_ _[∗]_ . All our applications of the SGR routine

6

(for this dataset and the rest) where with a particularly small confidence level _δ_ = 0 _._ 001. [3] We then applied these selective classifiers on the reserved test set, and computed, for each selective classifier,
_test risk_ and _test coverage_ . The results are summarized in Table 1, where we also include _train risk_ and _train coverage_ that were computed, for each selective classifier, over the training set.

Observing the results in Table 1, we see that the risk bound, _b_ _[∗]_, is always very close to the target risk,
_r_ _[∗]_ . Moreover, the test risk is always bounded above by the bound _b_ _[∗]_, as required. We compared this result to a basic baseline in which the threshold is defined to be the value that maximizes coverage while keeping train error smaller then _r_ _[∗]_ . For this simple baseline we found that in over 50% of the cases (1000 random train/test splits), the bound _r_ _[∗]_ was violated over the test set, with a mean violation of 18% relative to the requested _r_ _[∗]_ . Finally, we see that it is possible to guarantee with this method amazingly small 1% error while covering more than 78% of the domain.

**5.2** **Selective Guaranteed Risk for CIFAR-100**

Using the same VGG architechture (now adapted to 100 classes) we trained a model for CIFAR-100 while applying the same data augmentation routine as in the CIFAR-10 experiment. Following precisly the same experimental design as in the CFAR-10 case, we obtained the results of Table 2

Table 2: Risk control results for CIFAR-100 for _δ_ = 0 _._ 001

Desired risk ( _r_ _[∗]_ ) Train risk Train coverage Test risk Test coverage Risk bound ( _b_ _[∗]_ )

0.02 0.0119 0.2010 0.0187 0.2134 0.0197
0.05 0.0425 0.4286 0.0413 0.4450 0.0499
0.10 0.0927 0.5736 0.0938 0.5952 0.0998
0.15 0.1363 0.6546 0.1327 0.6752 0.1498
0.20 0.1872 0.7650 0.1810 0.7778 0.1999
0.25 0.2380 0.8716 0.2395 0.8826 0.2499

Here again, SGR generated tight bounds, very close to the desired target risk, and the bounds were never violated by the true risk. Also, we see again that it is possible to dramatically reduce the risk with only moderate compromise of the coverage. While the architecture we used is not state-of-the art, with a coverage of 67%, we easily surpassed the best known result for CIFAR-100, which currently stands on 18.85% using the wide residual network architecture [19]. It is very likely that by using ourselves the wide residual network architecture we could obtain significantly better results.

**5.3** **Selective Guaranteed Risk for ImageNet**

We used an already trained Image-Net VGG-16 model based on ILSVRC2014 [16]. We repeated the same experimental design but now the sizes of the training and test set were approximately 25,000.
The SGR results for both the top-1 and top-5 classification tasks are summarized in Tables 3 and 4, respectively. We also implemented the RESNET-50 architecture [12] in order to see if qualitatively similar results can be obtained with a different architecture. The RESNET-50 results for ImageNet top-1 and top-5 classification tasks are summarized in Tables 5 and 6, respectively.

Table 3: SGR results for Image-Net dataset using VGG-16 top-1 for _δ_ = 0 _._ 001

Desired risk ( _r_ _[∗]_ ) Train risk Train coverage Test risk Test coverage Risk bound( _b_ _[∗]_ )

0.02 0.0161 0.2355 0.0131 0.2322 0.0200
0.05 0.0462 0.4292 0.0446 0.4276 0.0500
0.10 0.0964 0.5968 0.0948 0.5951 0.1000
0.15 0.1466 0.7164 0.1467 0.7138 0.1500
0.20 0.1937 0.8131 0.1949 0.8154 0.2000
0.25 0.2441 0.9117 0.2445 0.9120 0.2500

3With this small _δ_, and small number of reported experiments (6-7 lines in each table) we did not perform a
Bonferroni correction (which can be easily added).

7

Table 4: SGR results for Image-Net dataset using VGG-16 top-5 for _δ_ = 0 _._ 001

Desired risk ( _r_ _[∗]_ ) Train risk Train coverage Test risk Test coverage Risk bound( _b_ _[∗]_ )

0.01 0.0080 0.3391 0.0078 0.3341 0.0100
0.02 0.0181 0.5360 0.0179 0.5351 0.0200
0.03 0.0281 0.6768 0.0290 0.6735 0.0300
0.04 0.0381 0.7610 0.0379 0.7586 0.0400
0.05 0.0481 0.8263 0.0496 0.8262 0.0500
0.06 0.0563 0.8654 0.0577 0.8668 0.0600
0.07 0.0663 0.9093 0.0694 0.9114 0.0700

Table 5: SGR results for Image-Net dataset using RESNET50 top-1 for _δ_ = 0 _._ 001

Desired risk ( _r_ _[∗]_ ) Train risk Train coverage Test risk Test coverage Risk bound ( _b_ _[∗]_ )

0.02 0.0161 0.2613 0.0164 0.2585 0.0199
0.05 0.0462 0.4906 0.0474 0.4878 0.0500
0.10 0.0965 0.6544 0.0988 0.6502 0.1000
0.15 0.1466 0.7711 0.1475 0.7676 0.1500
0.20 0.1937 0.8688 0.1955 0.8677 0.2000
0.25 0.2441 0.9634 0.2451 0.9614 0.2500

These results show that even for the challenging ImageNet, with both the VGG and RESNET architectures, our selective classifiers are extremely effective, and with appropriate coverage compromise, our classifier easily surpasses the best known results for ImageNet. Not surprisingly, RESNET, which is known to achieve better results than VGG on this set, preserves its relative advantage relative to
VGG through all _r_ _[∗]_ values.

**6** **Concluding Remarks**

We presented an algorithm for learning a selective classifier whose risk can be fully controlled and guaranteed with high confidence. Our empirical study validated this algorithm on challenging image classification datasets, and showed that guaranteed risk-control is achievable. Our methods can be immediately used by deep learning practitioners, helping them in coping with mission-critical tasks.

We believe that our work is only the first significant step in this direction, and many research questions are left open. The starting point in our approach is a trained neural classifier _f_ (supposedly trained to optimize risk under full coverage). While the rejection mechanisms we considered were extremely effective, it might be possible to identify superior mechanisms for a given classifier _f_ . We believe, however, that the most challenging open question would be to simultaneously train both the classifier
_f_ and the selection function _g_ to optimize coverage for a given risk level. Selective classification is intimately related to active learning in the context of linear classifiers [6, 11]. It would be very interesting to explore this potential relationship in the context of (deep) neural classification. In this paper we only studied selective classification under the 0/1 loss. It would be of great importance

Table 6: SGR results for Image-Net dataset using RESNET50 top-5 for _δ_ = 0 _._ 001

Desired risk ( _r_ _[∗]_ ) Train risk Train coverage Test risk Test coverage Risk bound( _b_ _[∗]_ )

0.01 0.0080 0.3796 0.0085 0.3807 0.0099
0.02 0.0181 0.5938 0.0189 0.5935 0.0200
0.03 0.0281 0.7122 0.0273 0.7096 0.0300
0.04 0.0381 0.8180 0.0358 0.8158 0.0400
0.05 0.0481 0.8856 0.0464 0.8846 0.0500
0.06 0.0581 0.9256 0.0552 0.9231 0.0600
0.07 0.0663 0.9508 0.0629 0.9484 0.0700

8

to extend our techniques to other loss functions and specifically to regression, and to fully control false-positive and false-negative rates.

This work has many applications. In general, any classification task where a controlled risk is critical would benefit by using our methods. An obvious example is that of medical applications where utmost precision is required and rejections should be handled by human experts. In such applications the existence of performance guarantees, as we propose here, is essential. Financial investment applications are also obvious, where there are great many opportunities from which one should cherry-pick the most certain ones. A more futuristic application is that of robotic sales representatives, where it could extremely harmful if the bot would try to answer questions it does not fully understand.

**Acknowledgments**

This research was supported by The Israel Science Foundation (grant No. 1890/14)

**References**

[1] Chao K Chow. An optimum character recognition system using decision functions. _IRE_

_Transactions on Electronic Computers_, (4):247–254, 1957.

[2] Luigi Pietro Cordella, Claudio De Stefano, Francesco Tortorella, and Mario Vento. A method

for improving classification reliability of multilayer perceptrons. _IEEE Transactions on Neural_
_Networks_, 6(5):1140–1147, 1995.

[3] Corinna Cortes, Giulia DeSalvo, and Mehryar Mohri. Boosting with abstention. In _Advances in_

_Neural Information Processing Systems_, pages 1660–1668, 2016.

[4] Claudio De Stefano, Carlo Sansone, and Mario Vento. To reject or not to reject: that is the

question-an answer in case of neural classifiers. _IEEE_ _Transactions_ _on_ _Systems,_ _Man,_ _and_
_Cybernetics, Part C (Applications and Reviews)_, 30(1):84–94, 2000.

[5] R. El-Yaniv and Y. Wiener. On the foundations of noise-free selective classification. _Journal of_

_Machine Learning Research_, 11:1605–1641, 2010.

[6] Ran El-Yaniv and Yair Wiener. Active learning via perfect selective classification. _Journal of_

_Machine Learning Research (JMLR)_, 13(Feb):255–279, 2012.

[7] Yoav Freund, Yishay Mansour, and Robert E Schapire. Generalization bounds for averaged

classifiers. _Annals of Statistics_, pages 1698–1722, 2004.

[8] Giorgio Fumera and Fabio Roli. Support vector machines with embedded reject option. In

_Pattern recognition with support vector machines_, pages 68–82. Springer, 2002.

[9] Yarin Gal and Zoubin Ghahramani. Dropout as a bayesian approximation: representing model

uncertainty in deep learning. In _Proceedings of The 33rd International Conference on Machine_
_Learning_, pages 1050–1059, 2016.

[10] O. Gascuel and G. Caraux. Distribution-free performance bounds with the resubstitution error

estimate. _Pattern Recognition Letters_, 13:757–764, 1992.

[11] R. Gelbhart and R. El-Yaniv. The Relationship Between Agnostic Selective Classification and

Active. _ArXiv e-prints_, January 2017.

[12] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for im age recognition. In _Proceedings_ _of_ _the_ _IEEE_ _Conference_ _on_ _Computer_ _Vision_ _and_ _Pattern_
_Recognition_, pages 770–778, 2016.

[13] Martin E Hellman. The nearest neighbor classification rule with a reject option. _IEEE Transac-_

_tions on Systems Science and Cybernetics_, 6(3):179–185, 1970.

[14] Alex Krizhevsky and Geoffrey Hinton. Learning multiple layers of features from tiny images.

2009.

9

[15] Shuying Liu and Weihong Deng. Very deep convolutional neural network based image classifi cation using small training sample size. In _Pattern Recognition (ACPR), 2015 3rd IAPR Asian_
_Conference on_, pages 730–734. IEEE, 2015.

[16] Olga Russakovsky, Jia Deng, Hao Su, Jonathan Krause, Sanjeev Satheesh, Sean Ma, Zhiheng

Huang, Andrej Karpathy, Aditya Khosla, Michael Bernstein, Alexander C. Berg, and Li Fei-Fei.
ImageNet large scale visual recognition challenge. _International Journal of Computer Vision_
_(IJCV)_, 115(3):211–252, 2015.

[17] Karen Simonyan and Andrew Zisserman. Very deep convolutional networks for large-scale

image recognition. _arXiv preprint arXiv:1409.1556_, 2014.

[18] Kush R Varshney. A risk bound for ensemble classification with a reject option. In _Statistical_

_Signal Processing Workshop (SSP), 2011 IEEE_, pages 769–772. IEEE, 2011.

[19] Sergey Zagoruyko and Nikos Komodakis. Wide residual networks. _arXiv_ _preprint_
_arXiv:1605.07146_, 2016.

10
