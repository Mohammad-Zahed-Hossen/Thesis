# **On Calibration of Modern Neural Networks**

**Chuan Guo** [* 1] **Geoff Pleiss** [* 1] **Yu Sun** [* 1] **Kilian Q. Weinberger** [1]

ResNet (2016)

CIFAR-100

**Abstract**

Confidence calibration – the problem of predicting probability estimates representative of the true correctness likelihood   - is important for classification models in many applications. We discover that modern neural networks, unlike those from a decade ago, are poorly calibrated.
Through extensive experiments, we observe that depth, width, weight decay, and Batch Normalization are important factors influencing calibration. We evaluate the performance of various post-processing calibration methods on state-ofthe-art architectures with image and document classification datasets. Our analysis and experiments not only offer insights into neural network learning, but also provide a simple and straightforward recipe for practical settings: on most datasets, _temperature_ _scaling_   - a singleparameter variant of Platt Scaling   - is surprisingly effective at calibrating predictions.

**1. Introduction**

Recent advances in deep learning have dramatically improved neural network accuracy (Simonyan & Zisserman,
2015; Srivastava et al., 2015; He et al., 2016; Huang et al.,
2016; 2017). As a result, neural networks are now entrusted with making complex decisions in applications, such as object detection (Girshick, 2015), speech recognition (Hannun et al., 2014), and medical diagnosis (Caruana et al.,
2015). In these settings, neural networks are an essential component of larger decision making pipelines.

In real-world decision making systems, classification networks must not only be accurate, but also should indicate when they are likely to be incorrect. As an example, consider a self-driving car that uses a neural network to detect pedestrians and other obstructions (Bojarski et al., 2016).

*Equal contribution, alphabetical order. 1Cornell University.
Correspondence to: Chuan Guo _<_ cg563@cornell.edu _>_, Geoff
Pleiss _<_ geoff@cs.cornell.edu _>_, Yu Sun _<_ ys646@cornell.edu _>_ .

_Proceedings_ _of_ _the_ _34_ _[th]_ _International_ _Conference_ _on_ _Machine_
_Learning_, Sydney, Australia, PMLR 70, 2017. Copyright 2017 by the author(s).

1 _._ 0

0 _._ 8

0 _._ 6

0 _._ 4

0 _._ 2

LeNet (1998)

CIFAR-100

0 _._ 0

|Col1|Col2|nce|Col4|acy|Col6|Col7|
|---|---|---|---|---|---|---|
|||ﬁde|||||
|||. con|<br>||||
|||Avg|||||
||||||||

0 _._ 0 0 _._ 2 0 _._ 4 0 _._ 6 0 _._ 8 1 _._ 0

1 _._ 0

|Col1|Col2|Col3|acy|Col5|nce|Col7|
|---|---|---|---|---|---|---|
||||cur||ﬁde||
||||A|<br>|. con||
||||||Avg||
||||||||

0 _._ 8

0 _._ 6

0 _._ 4

0 _._ 2

0 _._ 0

|Col1|Col2|Ou|Col4|tputs|Col6|Col7|Col8|Col9|Col10|Col11|
|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||
|||||~~p~~|~~p~~||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||E|r|ro|r=|r=|4|4.|9|
||||||||||||

0 _._ 0 0 _._ 2 0 _._ 4 0 _._ 6 0 _._ 8 1 _._ 0

0 _._ 0 0 _._ 2 0 _._ 4 0 _._ 6 0 _._ 8 1 _._ 0

|Col1|Col2|Ou|Col4|tputs|Col6|Col7|Col8|Col9|Col10|Col11|
|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||
|||||~~p~~|~~p~~||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||E|r|ro|r=|r=|3|0.|6|
||||||||||||

0 _._ 0 0 _._ 2 0 _._ 4 0 _._ 6 0 _._ 8 1 _._ 0

Confidence

_Figure 1._ Confidence histograms (top) and reliability diagrams
(bottom) for a 5-layer LeNet (left) and a 110-layer ResNet (right) on CIFAR-100. Refer to the text below for detailed illustration.

If the detection network is not able to confidently predict the presence or absence of immediate obstructions, the car should rely more on the output of other sensors for braking.
Alternatively, in automated health care, control should be passed on to human doctors when the confidence of a disease diagnosis network is low (Jiang et al., 2012). Specifically, a network should provide a _calibrated_ _confidence_ measure in addition to its prediction. In other words, the probability associated with the predicted class label should reflect its ground truth correctness likelihood.

Calibrated confidence estimates are also important for model interpretability. Humans have a natural cognitive intuition for probabilities (Cosmides & Tooby, 1996). Good confidence estimates provide a valuable extra bit of information to establish trustworthiness with the user - especially for neural networks, whose classification decisions are often difficult to interpret. Further, good probability estimates can be used to incorporate neural networks into other probabilistic models. For example, one can improve performance by combining network outputs with a lan

guage model in speech recognition (Hannun et al., 2014;
Xiong et al., 2016), or with camera information for object detection (Kendall & Cipolla, 2016).

In 2005, Niculescu-Mizil & Caruana (2005) showed that neural networks typically produce well-calibrated probabilities on binary classification tasks. While neural networks today are undoubtedly more accurate than they were a decade ago, we discover with great surprise that _mod-_
_ern_ _neural_ _networks_ _are_ _no_ _longer_ _well-calibrated_ . This is visualized in Figure 1, which compares a 5-layer LeNet
(left) (LeCun et al., 1998) with a 110-layer ResNet (right)
(He et al., 2016) on the CIFAR-100 dataset. The top row shows the distribution of prediction confidence (i.e. probabilities associated with the predicted label) as histograms.
The average confidence of LeNet closely matches its accuracy, while the average confidence of the ResNet is substantially higher than its accuracy. This is further illustrated in the bottom row reliability diagrams (DeGroot & Fienberg,
1983; Niculescu-Mizil & Caruana, 2005), which show accuracy as a function of confidence. We see that LeNet is well-calibrated, as confidence closely approximates the expected accuracy (i.e. the bars align roughly along the diagonal). On the other hand, the ResNet’s accuracy is better, but does not match its confidence.

Our goal is not only to understand why neural networks have become miscalibrated, but also to identify what methods can alleviate this problem. In this paper, we demonstrate on several computer vision and NLP tasks that neural networks produce confidences that cannot represent true probabilities. Additionally, we offer insight and intuition into network training and architectural trends that may cause miscalibration. Finally, we compare various postprocessing calibration methods on state-of-the-art neural networks, and introduce several extensions of our own.
Surprisingly, we find that a single-parameter variant of Platt scaling (Platt et al., 1999) - which we refer to as _temper-_
_ature_ _scaling_ - is often the most effective method at obtaining calibrated probabilities. Because this method is straightforward to implement with existing deep learning frameworks, it can be easily adopted in practical settings.

**2. Definitions**

The problem we address in this paper is supervised multiclass classification with neural networks. The input _X_ _∈X_ and label _Y_ _∈Y_ = _{_ 1 _, . . ., K}_ are random variables that follow a ground truth joint distribution _π_ ( _X, Y_ ) =
_π_ ( _Y |X_ ) _π_ ( _X_ ). Let _h_ be a neural network with _h_ ( _X_ ) =
( _Y,_ [ˆ] _P_ [ˆ] ), where _Y_ [ˆ] is a class prediction and _P_ [ˆ] is its associated confidence, i.e. probability of correctness. We would like the confidence estimate _P_ [ˆ] to be calibrated, which intuitively means that _P_ [ˆ] represents a true probability. For example, given 100 predictions, each with confidence of

Expected Calibration Error (Naeini et al., 2015) – or ECE

- approximates (2) by partitioning predictions into _M_
equally-spaced bins (similar to the reliability diagrams) and

0 _._ 8, we expect that 80 should be correctly classified. More formally, we define _perfect calibration_ as

P

_Y_ ˆ = _Y_ _|_ _P_ ˆ = _p_

= _p,_ _∀p ∈_ [0 _,_ 1] (1)

where the probability is over the joint distribution. In all practical settings, achieving perfect calibration is impossible. Additionally, the probability in (1) cannot be computed using finitely many samples since _P_ [ˆ] is a continuous random variable. This motivates the need for empirical approximations that capture the essence of (1).

**Reliability Diagrams** (e.g. Figure 1 bottom) are a visual representation of model calibration (DeGroot & Fienberg,
1983; Niculescu-Mizil & Caruana, 2005). These diagrams plot expected sample accuracy as a function of confidence.
If the model is perfectly calibrated – i.e. if (1) holds – then the diagram should plot the identity function. Any deviation from a perfect diagonal represents miscalibration.

To estimate the expected accuracy from finite samples, we group predictions into _M_ interval bins (each of size 1 _/M_ ) and calculate the accuracy of each bin. Let _Bm_ be the set of indices of samples whose prediction confidence falls into the interval _Im_ = ( _[m]_ _M_ _[−]_ [1] _[,]_ _M_ _[m]_ []][.] [The accuracy of] _[ B][m]_ [ is]

_M_ _[m]_ []][.] [The accuracy of] _[ B][m]_ [ is]

_[−]_ [1] _[m]_

_M_ _[,]_ _M_

1 acc( _Bm_ ) =
_Bm_
_|_ _|_

_i∈Bm_

_∈_ - _Bm_

**1** (ˆ _yi_ = _yi_ ) _,_

where _y_ ˆ _i_ and _yi_ are the predicted and true class labels for sample _i_ . Basic probability tells us that acc( _Bm_ ) is an unbiased and consistent estimator of P( _Y_ [ˆ] = _Y_ _|_ _P_ [ˆ] _∈_ _Im_ ).
We define the average confidence within bin _Bm_ as

1 conf( _Bm_ ) =
_Bm_
_|_ _|_

_i∈Bm_

_∈_ - _Bm_

_p_ ˆ _i,_

where _p_ ˆ _i_ is the confidence for sample _i_ . acc( _Bm_ ) and conf( _Bm_ ) approximate the left-hand and right-hand sides of (1) respectively for bin _Bm_ . Therefore, a perfectly calibrated model will have acc( _Bm_ ) = conf( _Bm_ ) for all
_m ∈{_ 1 _, . . ., M_ _}_ . Note that reliability diagrams do not display the proportion of samples in a given bin, and thus cannot be used to estimate how many samples are calibrated.

**Expected** **Calibration** **Error** **(ECE).** While reliability diagrams are useful visual tools, it is more convenient to have a scalar summary statistic of calibration. Since statistics comparing two distributions cannot be comprehensive, previous works have proposed variants, each with a unique emphasis. One notion of miscalibration is the difference in expectation between confidence and accuracy, i.e.

P _Y_ ˆ = _Y_ _|_ _P_ ˆ = _p_
����

(2)

2015) – or ECE

���

E

_P_ ˆ

E

_−_ _p_

Varying Width
ResNet-14 - CIFAR-100

|Col1|Col2|Col3|Col4|Col5|Col6|ror|Col8|
|---|---|---|---|---|---|---|---|
||||||Er|ror|ror|
||||||EC|E||
|||||||||
|||||||||
|||||||||
|||||||||
|||||||||

0 50 100 150 200 250 300
Filters per layer

Using Normalization
ConvNet - CIFAR-100

|Col1|Col2|Col3|Col4|Col5|Col6|Error|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
|||||||Error|Error|Error|
|||||||ECE|ECE||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||

Without With
Batch Normalization

Varying Weight Decay
ResNet-110 - CIFAR-100

|Col1|Col2|Col3|Error|Col5|
|---|---|---|---|---|
||||Error|Error|
||||ECE||
||||||
||||||
||||||
||||||
||||||

10 _[−]_ [5] 10 _[−]_ [4] 10 _[−]_ [3] 10 _[−]_ [2]

Weight decay

0 _._ 7

0 _._ 6

0 _._ 5

0 _._ 4

0 _._ 3

0 _._ 2

0 _._ 1

0 _._ 0

Varying Depth
ResNet - CIFAR-100

|Col1|Col2|Col3|Col4|Col5|ror|Col7|
|---|---|---|---|---|---|---|
|||||Er|ror|ror|
|||||EC|E||
||||||||
||||||||
||||||||
||||||||
||||||||

0 20 40 60 80 100 120
Depth

_Figure 2._ The effect of network depth (far left), width (middle left), Batch Normalization (middle right), and weight decay (far right) on miscalibration, as measured by ECE (lower is better).

taking a weighted average of the bins’ accuracy/confidence difference. More precisely,

acc( _Bm_ ) conf( _Bm_ ) _,_ (3)
_−_

The difference between

���� ����

ECE =

_M_

_m_ =1

_m_ =1

_Bm_
_|_ _|_

_n_

where _n_ is the number of samples. The difference between acc and conf for a given bin represents the calibration _gap_
(red bars in reliability diagrams - e.g. Figure 1). We use
ECE as the primary empirical metric to measure calibration. See Section S1 for more analysis of this metric.

**Maximum** **Calibration** **Error** **(MCE).** In high-risk applications where reliable confidence measures are absolutely necessary, we may wish to minimize the worst-case deviation between confidence and accuracy:

**3. Observing Miscalibration**

The architecture and training procedures of neural networks have rapidly evolved in recent years. In this section we identify some recent changes that are responsible for the miscalibration phenomenon observed in Figure 1.
Though we cannot claim causality, we find that model capacity and lack of regularization are closely related to model (mis)calibration.

**Model capacity.** The model capacity of neural networks has increased at a dramatic pace over the past few years.
It is now common to see networks with hundreds, if not thousands of layers (He et al., 2016; Huang et al., 2016) and hundreds of convolutional filters per layer (Zagoruyko
& Komodakis, 2016). Recent work shows that very deep or wide models are able to generalize better than smaller ones, while exhibiting the capacity to easily fit the training set (Zhang et al., 2017).

Although increasing depth and width may reduce classification error, we observe that these increases negatively affect model calibration. Figure 2 displays error and ECE as a function of depth and width on a ResNet trained on
CIFAR-100. The far left figure varies depth for a network with 64 convolutional filters per layer, while the middle left figure fixes the depth at 14 layers and varies the number of convolutional filters per layer. Though even the smallest models in the graph exhibit some degree of miscalibration, the ECE metric grows substantially with model capacity. During training, after the model is able to correctly classify (almost) all training samples, NLL can be further minimized by increasing the confidence of predictions. Increased model capacity will lower training NLL, and thus the model will be more (over)confident on average.

**Batch Normalization** (Ioffe & Szegedy, 2015) improves the optimization of neural networks by minimizing distribution shifts in activations within the neural network’s hid

_._ (4)

, 2015) – or

���

max
_p∈_ [0 _,_ 1]

P _Y_ ˆ = _Y_ _|_ _P_ ˆ = _p_
���

_−_ _p_

The Maximum Calibration Error (Naeini et al., 2015) – or
MCE - estimates an upper bound of this deviation. Similarly to ECE, this approximation involves binning:

MCE = max (5)
_m∈{_ 1 _,...,M_ _}_ _[|]_ [acc(] _[B][m]_ [)] _[ −]_ [conf(] _[B][m]_ [)] _[|][ .]_

In reliability diagrams, MCE measures the largest calibration gap (red bars) across all bins, whereas ECE measures a weighted average of all gaps. For perfectly calibrated classifiers, MCE and ECE both equal 0.

MCE = max (5)
_m∈{_ 1 _,...,M_ _}_ _[|]_ [acc(] _[B][m]_ [)] _[ −]_ [conf(] _[B][m]_ [)] _[|][ .]_

**Negative log likelihood** is a standard measure of a probabilistic model’s quality (Friedman et al., 2001). It is also referred to as the cross entropy loss in the context of deep learning (Bengio et al., 2015). Given a probabilistic model

_π_ ˆ( _Y |X_ ) and _n_ samples, NLL is defined as:

_L_ = _−_

_n_

_i_ =1

_i_ =1

log(ˆ _π_ ( _yi_ **x** _i_ )) (6)
_|_

It is a standard result (Friedman et al., 2001) that, in expectation, NLL is minimized if and only if _π_ ˆ( _Y |X_ ) recovers the ground truth conditional distribution _π_ ( _Y |X_ ).

NLL Overfitting on CIFAR−100

45

40

35

30

25

20
0 100 200 300 400 500

Epoch

_Figure 3._ Test error and NLL of a 110-layer ResNet with stochastic depth on CIFAR-100 during training. NLL is scaled by a constant to fit in the figure. Learning rate drops by 10x at epochs 250 and 375. The shaded area marks between epochs at which the best validation _loss_ and best validation _error_ are produced.

den layers. Recent research suggests that these normalization techniques have enabled the development of very deep architectures, such as ResNets (He et al., 2016) and
DenseNets (Huang et al., 2017). It has been shown that
Batch Normalization improves training time, reduces the need for additional regularization, and can in some cases improve the accuracy of networks.

While it is difficult to pinpoint exactly how Batch Normalization affects the final predictions of a model, we do observe that models trained with Batch Normalization tend to be more miscalibrated. In the middle right plot of Figure 2, we see that a 6-layer ConvNet obtains worse calibration when Batch Normalization is applied, even though classification accuracy improves slightly. We find that this result holds regardless of the hyperparameters used on the Batch
Normalization model (i.e. low or high learning rate, etc.).

**Weight** **decay,** which used to be the predominant regularization mechanism for neural networks, is decreasingly utilized when training modern neural networks. Learning theory suggests that regularization is necessary to prevent overfitting, especially as model capacity increases (Vapnik,
1998). However, due to the apparent regularization effects of Batch Normalization, recent research seems to suggest that models with less L2 regularization tend to generalize better (Ioffe & Szegedy, 2015). As a result, it is now common to train models with little weight decay, if any at all.
The top performing ImageNet models of 2015 all use an order of magnitude less weight decay than models of previous years (He et al., 2016; Simonyan & Zisserman, 2015).

We find that training with less weight decay has a negative impact on calibration. The far right plot in Figure 2 dis

plays training error and ECE for a 110-layer ResNet with varying amounts of weight decay. The only other forms of regularization are data augmentation and Batch Normalization. We observe that calibration and accuracy are not optimized by the same parameter setting. While the model exhibits both over-regularization and under-regularization with respect to classification error, it does not appear that calibration is negatively impacted by having too much weight decay. Model calibration continues to improve when more regularization is added, well after the point of achieving optimal accuracy. The slight uptick at the end of the graph may be an artifact of using a weight decay factor that impedes optimization.

**NLL** can be used to indirectly measure model calibration. In practice, we observe _a_ _disconnect_ _between_ _NLL_
_and accuracy_, which may explain the miscalibration in Figure 2. This disconnect occurs because neural networks can
_overfit_ _to_ _NLL_ _without_ _overfitting_ _to_ _the_ _0/1_ _loss_ . We observe this trend in the training curves of some miscalibrated models. Figure 3 shows test error and NLL (rescaled to match error) on CIFAR-100 as training progresses. Both error and NLL immediately drop at epoch 250, when the learning rate is dropped; however, NLL overfits during the remainder of training. Surprisingly, overfitting to NLL is beneficial to classification accuracy. On CIFAR-100, test error drops from 29% to 27% in the region where NLL overfits. This phenomenon renders a concrete explanation of miscalibration: the network learns better classification accuracy at the expense of well-modeled probabilities.

We can connect this finding to recent work examining the generalization of large neural networks. Zhang et al. (2017) observe that deep neural networks seemingly violate the common understanding of learning theory that large models with little regularization will not generalize well. The observed disconnect between NLL and 0/1 loss suggests that these high capacity models are not necessarily immune from overfitting, but rather, overfitting manifests in probabilistic error rather than classification error.

**4. Calibration Methods**

In this section, we first review existing calibration methods, and introduce new variants of our own. All methods are post-processing steps that produce (calibrated) probabilities. Each method requires a hold-out validation set, which in practice can be the same set used for hyperparameter tuning. We assume that the training, validation, and test sets are drawn from the same distribution.

**4.1. Calibrating Binary Models**

We first introduce calibration in the binary setting, i.e.
_Y_ = _{_ 0 _,_ 1 _}_ . For simplicity, throughout this subsection,

we assume the model outputs only the confidence for the positive class. [1] Given a sample **x** _i_, we have access to _p_ ˆ _i_ the network’s predicted probability of _yi_ = 1, as well as
_zi_ _∈_ R - which is the network’s non-probabilistic output, or _logit_ . The predicted probability _p_ ˆ _i_ is derived from _zi_ using a sigmoid function _σ_ ; i.e. _p_ ˆ _i_ = _σ_ ( _zi_ ). Our goal is to produce a calibrated probability _q_ ˆ _i_ based on _yi_, _p_ ˆ _i_, and _zi_ .

**Histogram binning** (Zadrozny & Elkan, 2001) is a simple non-parametric calibration method. In a nutshell, all uncalibrated predictions _p_ ˆ _i_ are divided into mutually exclusive bins _B_ 1 _, . . ., BM_ . Each bin is assigned a calibrated score _θm_ ; i.e. if _p_ ˆ _i_ is assigned to bin _Bm_, then _q_ ˆ _i_ = _θm_ . At test time, if prediction _p_ ˆ _te_ falls into bin _Bm_, then the calibrated prediction _q_ ˆ _te_ is _θm_ . More precisely, for a suitably chosen _M_ (usually small), we first define bin boundaries
0 = _a_ 1 _a_ 2 _. . ._ _aM_ +1 = 1, where the bin _Bm_
_≤_ _≤_ _≤_ is defined by the interval ( _am, am_ +1]. Typically the bin boundaries are either chosen to be equal length intervals or to equalize the number of samples in each bin. The predictions _θi_ are chosen to minimize the bin-wise squared loss:

model averaging. Essentially, BBQ marginalizes out all possible _binning schemes_ to produce _q_ ˆ _i_ . More formally, a binning scheme _s_ is a pair ( _M, I_ ) where _M_ is the number of bins, and _I_ is a corresponding partitioning of [0 _,_ 1] into disjoint intervals (0 = _a_ 1 _a_ 2 _. . ._ _aM_ +1 = 1). The
_≤_ _≤_ _≤_ parameters of a binning scheme are _θ_ 1 _, . . ., θM_ . Under this framework, histogram binning and isotonic regression both produce a single binning scheme, whereas BBQ considers a space _S_ of all possible binning schemes for the validation dataset _D_ . BBQ performs Bayesian averaging of the probabilities produced by each scheme: [2]

_s_ _[′]_ _∈S_ [P][(] _[D]_ _[|][ S]_ [ =] _[s][′]_ [)] _[.]_

P(ˆ _qte_ _|_ _p_ ˆ _te, D_ ) =

=

_s_ - _∈S_

_s∈S_

_s_ - _∈S_

_s∈S_

P(ˆ _qte, S_ = _s |_ _p_ ˆ _te, D_ )

P(ˆ _qte_ _|_ _p_ ˆ _te, S_ = _s, D_ ) P( _S_ = _s | D_ ) _._

where P(ˆ _qte_ _|_ _p_ ˆ _te, S_ = _s, D_ ) is the calibrated probability using binning scheme _s_ . Using a uniform prior, the weight
P( _S_ = _s | D_ ) can be derived using Bayes’ rule:

The parameters _θ_ 1 _, . . ., θM_ can be viewed as parameters of
_M_ independent binomial distributions. Hence, by placing a Beta prior on _θ_ 1 _, . . ., θM_, we can obtain a closed form expression for the marginal likelihood P( _D_ _|_ _S_ = _s_ ). This allows us to compute P(ˆ _qte_ _|_ _p_ ˆ _te, D_ ) for any test input.

**Platt scaling** (Platt et al., 1999) is a parametric approach to calibration, unlike the other approaches. The nonprobabilistic predictions of a classifier are used as features for a logistic regression model, which is trained on the validation set to return probabilities. More specifically, in the context of neural networks (Niculescu-Mizil & Caruana,
2005), Platt scaling learns scalar parameters _a, b_ _∈_ R and outputs _q_ ˆ _i_ = _σ_ ( _azi_ + _b_ ) as the calibrated probability. Parameters _a_ and _b_ can be optimized using the NLL loss over the validation set. It is important to note that the neural network’s parameters are fixed during this stage.

**4.2. Extension to Multiclass Models**

For classification problems involving _K_ _>_ 2 classes, we return to the original problem formulation. The network outputs a class prediction _y_ ˆ _i_ and confidence score _p_ ˆ _i_ for each input **x** _i_ . In this case, the network logits **z** _i_ are vectors, where ˆ _yi_ = argmax _k zi_ [(] _[k]_ [)], and _p_ ˆ _i_ is typically derived using

the softmax function _σ_ SM:

P( _D_ _S_ = _s_ )
P( _S_ = _s | D_ ) = _s_ _[′]_ _∈S_ [P][(] _|_ _[D]_ _[|][ S]_

_θ_ 1 _, . . ., θM_

~~�~~

min
_θ_ 1 _,...,θM_

_M_

_m_ =1

_m_ =1

_n_

_i_ =1

_i_ =1

**1** ( _am_ _p_ ˆ _i_ _< am_ +1) ( _θm_ _yi_ ) [2] _,_ (7)
_≤_ _−_

where **1** is the indicator function. Given fixed bins boundaries, the solution to (7) results in _θm_ that correspond to the average number of positive-class samples in bin _Bm_ .

**Isotonic regression** (Zadrozny & Elkan, 2002), arguably the most common non-parametric calibration method, learns a piecewise constant function _f_ to transform uncalibrated outputs; i.e. _q_ ˆ _i_ = _f_ (ˆ _pi_ ). Specifically, isotonic regression produces _f_ to minimize the square loss
_ni_ =1 [(] _[f]_ [(ˆ] _[p][i]_ [)] _[ −]_ _[y][i]_ [)][2][.] [Because] _[ f]_ [is constrained to be piece-] wise constant, we can write the optimization problem as:

min

_M_
_θ_ 1 _,...,θM_
_a_ 1 _,...,aM_ +1

_M_ _n_

_m_ =1 _i_ =1

-

**1** ( _am_ _p_ ˆ _i_ _< am_ +1) ( _θm_ _yi_ ) [2]
_≤_ _−_

subject to 0 = _a_ 1 _a_ 2 _. . ._ _aM_ +1 = 1 _,_
_≤_ _≤_ _≤_

_θ_ 1 _θ_ 2 _. . ._ _θM_ _._
_≤_ _≤_ _≤_

where _M_ is the number of intervals; _a_ 1 _, . . ., aM_ +1 are the interval boundaries; and _θ_ 1 _, . . ., θM_ are the function values. Under this parameterization, isotonic regression is a strict generalization of histogram binning in which the bin boundaries and bin predictions are jointly optimized.

_σ_ SM( **z** _i_ ) [(] _[k]_ [)] = exp( _zi_ [(] _[k]_ [)]

_i_ )

_,_ _p_ ˆ _i_ = max _σ_ SM( **z** _i_ ) [(] _[k]_ [)] _._

_k_

**Bayesian Binning into Quantiles (BBQ)** (Naeini et al.,
2015) is a extension of histogram binning using Bayesian

1 This is in contrast with the setting in Section 2, in which the model produces both a class prediction and confidence.

2 Because the validation dataset is finite, _S_ is as well.

exp( _zi_ )

_K_
_j_ =1 [exp(] _[z]_ _i_ [(] _[j]_ [)]

~~�~~

The goal is to produce a calibrated confidence _q_ ˆ _i_ and (possibly new) class prediction _y_ ˆ _i_ _[′]_ [based on] _[ y][i]_ [,] _[y]_ [ˆ] _[i]_ [,] _[p]_ [ˆ] _[i]_ [, and] **[ z]** _[i]_ [.]

_i_ _[′]_ [based on] _[ y][i]_ [,] _[y]_ [ˆ] _[i]_ [,] _[p]_ [ˆ] _[i]_ [, and] **[ z]** _[i]_ [.]

Dataset Model Uncalibrated Hist. Binning Isotonic BBQ Temp. Scaling Vector Scaling Matrix Scaling

Birds ResNet 50 9.19% 4.34% 5.22% 4.12% **1.85%** 3.0% 21.13%
Cars ResNet 50 4.3% **1.74%** 4.29% 1.84% 2.35% 2.37% 10.5%
CIFAR-10 ResNet 110 4.6% 0.58% 0.81% **0.54%** 0.83% 0.88% 1.0%
CIFAR-10 ResNet 110 (SD) 4.12% 0.67% 1.11% 0.9% **0.6%** 0.64% 0.72%
CIFAR-10 Wide ResNet 32 4.52% 0.72% 1.08% 0.74% **0.54%** 0.6% 0.72%
CIFAR-10 DenseNet 40 3.28% 0.44% 0.61% 0.81% **0.33%** 0.41% 0.41%
CIFAR-10 LeNet 5 3.02% 1.56% 1.85% 1.59% **0.93%** 1.15% 1.16%
CIFAR-100 ResNet 110 16.53% 2.66% 4.99% 5.46% **1.26%** 1.32% 25.49%
CIFAR-100 ResNet 110 (SD) 12.67% 2.46% 4.16% 3.58% 0.96% **0.9%** 20.09%
CIFAR-100 Wide ResNet 32 15.0% 3.01% 5.85% 5.77% **2.32%** 2.57% 24.44%
CIFAR-100 DenseNet 40 10.37% 2.68% 4.51% 3.59% 1.18% **1.09%** 21.87%
CIFAR-100 LeNet 5 4.85% 6.48% 2.35% 3.77% **2.02%** 2.09% 13.24%
ImageNet DenseNet 161 6.28% 4.52% 5.18% 3.51% **1.99%** 2.24%   ImageNet ResNet 152 5.48% 4.36% 4.77% 3.56% **1.86%** 2.23%   SVHN ResNet 152 (SD) 0.44% **0.14%** 0.28% 0.22% 0.17% 0.27% 0.17%

20 News DAN 3 8.02% **3.6%** 5.52% 4.98% 4.11% 4.61% 9.1%
Reuters DAN 3 0.85% 1.75% 1.15% 0.97% 0.91% **0.66%** 1.58%
SST Binary TreeLSTM 6.63% 1.93% **1.65%** 2.27% 1.84% 1.84% 1.84%
SST Fine Grained TreeLSTM 6.71% 2.09% **1.65%** 2.61% 2.56% 2.98% 2.39%

_Table 1._ ECE (%) (with _M_ = 15 bins) on standard vision and NLP datasets before calibration and with various calibration methods.
The number following a model’s name denotes the network depth.

**Extension of binning methods.** One common way of extending binary calibration methods to the multiclass setting is by treating the problem as _K_ one-versus-all problems
(Zadrozny & Elkan, 2002). For _k_ = 1 _, . . ., K_, we form a binary calibration problem where the label is **1** ( _yi_ = _k_ ) and the predicted probability is _σ_ SM( **z** _i_ ) [(] _[k]_ [)] . This gives us _K_ calibration models, each for a particular class. At test time, we obtain an unnormalized probability vector

[ˆ _q_ [(1)] _, . . .,_ ˆ _q_ [(] _[K]_ [)] ], where _q_ ˆ [(] _[k]_ [)] is the calibrated probability for

_i_ [(1)] _, . . .,_ ˆ _qi_ [(] _[K]_ [)]

_i_ [(] _[K]_ [)] ], where _q_ ˆ _i_ [(] _[k]_ [)]

[ˆ _qi_ [(1)] _, . . .,_ ˆ _qi_ [(] _[K]_ [)] ], where _q_ ˆ _i_ [(] _[k]_ [)] is the calibrated probability for

class _k_ . The new class prediction _y_ ˆ _i_ _[′]_ [is] [the] [argmax] [of] [the]

class _k_ . The new class prediction _y_ ˆ _i_ _[′]_ [is] [the] [argmax] [of] [the]

vector, and the new confidence _q_ ˆ _i_ _[′]_ [is the max of the vector]

vector, and the new confidence _q_ ˆ _i_ _[′]_ [is the max of the vector]

normalized by _k_ =1 _[q]_ [ˆ] _i_ [(] _[k]_ [)] . This extension can be applied

to histogram binning, isotonic regression, and BBQ.

[�] _[K]_

_k_ _[K]_ =1 _[q]_ [ˆ] _i_ [(] _[k]_ [)]

normalized by _k_ =1 _[q]_ [ˆ] _i_ [(] _[k]_ [)] . This extension can be applied

to histogram binning, isotonic regression, and BBQ.

_[K]_

**Matrix** **and** **vector** **scaling** are two multi-class extensions of Platt scaling. Let **z** _i_ be the _logits vector_ produced before the softmax layer for input **x** _i_ . _Matrix_ _scaling_ _ap-_
_plies_ a linear transformation **Wz** _i_ + **b** to the logits:

_σ_ SM( **Wz** _i_ + **b** ) [(] _[k]_ [)] _,_
_k_

_q_ ˆ _i_ = max

_T_ is called the temperature, and it “softens” the softmax
(i.e. raises the output entropy) with _T_ _>_ 1. As _T_ _→∞_, the probability _q_ ˆ _i_ approaches 1 _/K_, which represents maximum uncertainty. With _T_ = 1, we recover the original probability _p_ ˆ _i_ . As _T_ 0, the probability collapses to a
_→_ point mass (i.e. _q_ ˆ _i_ = 1). _T_ is optimized with respect to
NLL on the validation set. Because the parameter _T_ does not change the maximum of the softmax function, the class prediction _y_ ˆ _i_ _[′]_ [remains unchanged.] [In other words,] _[temper-]_

_ature scaling does not affect the model’s accuracy._

Temperature scaling is commonly used in settings such as knowledge distillation (Hinton et al., 2015) and statistical mechanics (Jaynes, 1957). To the best of our knowledge, we are not aware of any prior use in the context of calibrating probabilistic models. [3] The model is equivalent to maximizing the entropy of the output probability distribution subject to certain constraints on the logits (see Section S2).

**4.3. Other Related Works**

Calibration and confidence scores have been studied in various contexts in recent years. Kuleshov & Ermon (2016) study the problem of calibration in the online setting, where the inputs can come from a potentially adversarial source.
Kuleshov & Liang (2015) investigate how to produce calibrated probabilities when the output space is a structured object. Lakshminarayanan et al. (2016) use ensembles of networks to obtain uncertainty estimates. Pereyra et al.
(2017) penalize overconfident predictions as a form of regularization. Hendrycks & Gimpel (2017) use confidence

3To highlight the connection with prior works we define temperature scaling in terms of _T_ [1] [instead of a multiplicative scalar.]

_y_ ˆ _[′]_

_i_ _[′]_ [= argmax]

(8)
( **Wz** _i_ + **b** ) [(] _[k]_ [)] _._

_k_

The parameters **W** and **b** are optimized with respect to
NLL on the validation set. As the number of parameters for matrix scaling grows quadratically with the number of classes _K_, we define _vector scaling_ as a variant where **W** is restricted to be a diagonal matrix.

**Temperature** **scaling,** the simplest extension of Platt scaling, uses a single scalar parameter _T_ _>_ 0 for all classes.
Given the logit vector **z** _i_, the new confidence prediction is

_q_ ˆ _i_ = max _σ_ SM( **z** _i/T_ ) [(] _[k]_ [)] _._ (9)

_k_

scores to determine if samples are out-of-distribution.

Bayesian neural networks (Denker & Lecun, 1990;
MacKay, 1992) return a probability distribution over outputs as an alternative way to represent model uncertainty.
Gal & Ghahramani (2016) draw a connection between
Dropout (Srivastava et al., 2014) and model uncertainty, claiming that sampling models with dropped nodes is a way to estimate the probability distribution over all possible models for a given sample. Kendall & Gal (2017) combine this approach with a model that outputs a predictive mean and variance for each data point. This notion of uncertainty is not restricted to classification problems.
In contrast, our framework, which does not require model sampling, returns a confidence for a given output rather than returning a distribution of possible outputs.

**5. Results**

We apply the calibration methods in Section 4 to image classification and document classification neural networks.
For image classification we use 6 datasets:

1. Caltech-UCSD Birds (Welinder et al., 2010):
200 bird species. 5994/2897/2897 images for train/validation/test sets.
2. Stanford Cars (Krause et al., 2013): 196 classes of
cars by make, model, and year. 8041/4020/4020 images for train/validation/test.
3. ImageNet 2012 (Deng et al., 2009): Natural scene images from 1000 classes. 1.3 million/25,000/25,000
images for train/validation/test.
4. CIFAR-10/CIFAR-100 (Krizhevsky & Hinton, 2009):
Color images (32 _×_ 32) from 10/100 classes.
45,000/5,000/10,000 images for train/validation/test.
5. Street View House Numbers (SVHN) (Netzer et al.,
2011): 32 _×_ 32 colored images of cropped out house numbers from Google Street View.
604,388/6,000/26,032 images for train/validation/test.

We train state-of-the-art convolutional networks: ResNets
(He et al., 2016), ResNets with stochastic depth (SD)
(Huang et al., 2016), Wide ResNets (Zagoruyko & Komodakis, 2016), and DenseNets (Huang et al., 2017). We use the data preprocessing, training procedures, and hyperparameters as described in each paper. For Birds and Cars, we fine-tune networks pretrained on ImageNet.

For document classification we experiment with 4 datasets:

1. 20 News: News articles, partitioned into 20 categories by content. 9034/2259/7528 documents for
train/validation/test.
2. Reuters: News articles, partitioned into 8 categories by topic. 4388/1097/2189 documents for
train/validation/test.

3. Stanford Sentiment Treebank (SST) (Socher et al.,
2013): Movie reviews, represented as sentence parse trees that are annotated by sentiment. Each sample includes a coarse binary label and a fine grained 5-class label. As described in (Tai et al., 2015), the training/validation/test sets contain 6920/872/1821 documents for binary, and 544/1101/2210 for fine-grained.

On 20 News and Reuters, we train Deep Averaging Networks (DANs) (Iyyer et al., 2015) with 3 feed-forward layers and Batch Normalization. These networks obtain competitive accuracy using the optimization hyperparameters suggested by the original paper. On SST, we train
TreeLSTMs (Long Short Term Memory) (Tai et al., 2015) using the default settings in the authors’ code.

**Calibration Results.** Table 1 displays model calibration, as measured by ECE (with _M_ = 15 bins), before and after applying the various methods (see Section S3 for MCE,
NLL, and error tables). It is worth noting that most datasets and models experience some degree of miscalibration, with
ECE typically between 4 to 10%. This is not architecture specific: we observe miscalibration on convolutional networks (with and without skip connections), recurrent networks, and deep averaging networks. The two notable exceptions are SVHN and Reuters, both of which experience
ECE values below 1%. Both of these datasets have very low error (1 _._ 98% and 2 _._ 97%, respectively); and therefore the ratio of ECE to error is comparable to other datasets.

Our most important discovery is the _surprising_ _effective-_
_ness of temperature scaling_ despite its remarkable simplicity. Temperature scaling outperforms all other methods on the vision tasks, and performs comparably to other methods on the NLP datasets. What is perhaps even more surprising is that temperature scaling outperforms the vector and matrix Platt scaling variants, which are strictly more general methods. In fact, vector scaling recovers essentially the same solution as temperature scaling – the learned vector has nearly constant entries, and therefore is no different than a scalar transformation. In other words, network miscalibration is intrinsically low dimensional.

The only dataset that temperature scaling does not calibrate is the Reuters dataset. In this instance, only one of the above methods is able to improve calibration. Because this dataset is well-calibrated to begin with (ECE _≤_ 1%), there is not much room for improvement with any method, and post-processing may not even be necessary to begin with.
It is also possible that our measurements are affected by dataset split or by the particular binning scheme.

Matrix scaling performs poorly on datasets with hundreds of classes (i.e. Birds, Cars, and CIFAR-100), and fails to converge on the 1000-class ImageNet dataset. This is expected, since the number of parameters scales quadrat

|Col1|Col2|Ou<br>Ga|Col4|tputs<br>p|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||E|C|E|=2|.4|6|
|||||||||||

0 _._ 0 0 _._ 2 0 _._ 4 0 _._ 6 0 _._ 8 1 _._ 0

|Col1|Col2|Ou<br>Ga|Col4|tputs<br>p|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||E|C|E|=4|.1|6|
|||||||||||

0 _._ 0 0 _._ 2 0 _._ 4 0 _._ 6 0 _._ 8 1 _._ 0

|Col1|Col2|Ou<br>Ga|Col4|Col5|tputs<br>p|Col7|Col8|Col9|Col10|Col11|
|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||||||||||
||||||EC|E|=|12|.6|7|

0 _._ 0 0 _._ 2 0 _._ 4 0 _._ 6 0 _._ 8 1 _._ 0

|Col1|Col2|Ou<br>Ga|Col4|tputs<br>p|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||E|C|E|=0|.9|6|
|||||||||||

0 _._ 0 0 _._ 2 0 _._ 4 0 _._ 6 0 _._ 8 1 _._ 0

Confidence

_Figure 4._ Reliability diagrams for CIFAR-100 before (far left) and after calibration (middle left, middle right, far right).

ically with the number of classes. Any calibration model with tens of thousands (or more) parameters will overfit to a small validation set, even when applying regularization.

Binning methods improve calibration on most datasets, but do not outperform temperature scaling. Additionally, binning methods tend to change class predictions which hurts accuracy (see Section S3). Histogram binning, the simplest binning method, typically outperforms isotonic regression and BBQ, despite the fact that both methods are strictly more general. This further supports our finding that calibration is best corrected by simple models.

**Reliability** **diagrams.** Figure 4 contains reliability diagrams for 110-layer ResNets on CIFAR-100 before and after calibration. From the far left diagram, we see that the uncalibrated ResNet tends to be overconfident in its predictions. We then can observe the effects of temperature scaling (middle left), histogram binning (middle right), and isotonic regression (far right) on calibration. All three displayed methods produce much better confidence estimates.
Of the three methods, temperature scaling most closely recovers the desired diagonal function. Each of the bins are well calibrated, which is remarkable given that all the probabilities were modified by only a single parameter. We include reliability diagrams for other datasets in Section S4.

**Computation** **time.** All methods scale linearly with the number of validation set samples. Temperature scaling is by far the fastest method, as it amounts to a onedimensional convex optimization problem. Using a conjugate gradient solver, the optimal temperature can be found in 10 iterations, or a fraction of a second on most modern hardware. In fact, even a naive line-search for the optimal temperature is faster than any of the other methods. The computational complexity of vector and matrix scaling are linear and quadratic respectively in the number of classes, reflecting the number of parameters in each method. For
CIFAR-100 ( _K_ = 100), finding a near-optimal vector scal

ing solution with conjugate gradient descent requires at least 2 orders of magnitude more time. Histogram binning and isotonic regression take an order of magnitude longer than temperature scaling, and BBQ takes roughly 3 orders of magnitude more time.

**Ease of implementation.** BBQ is arguably the most difficult to implement, as it requires implementing a model averaging scheme. While all other methods are relatively easy to implement, temperature scaling may arguably be the most straightforward to incorporate into a neural network pipeline. In Torch7 (Collobert et al., 2011), for example, we implement temperature scaling by inserting a nn.MulConstant between the logits and the softmax, whose parameter is 1 _/T_ . We set _T_ =1 during training, and subsequently find its optimal value on the validation set.

**6. Conclusion**

Modern neural networks exhibit a strange phenomenon:
probabilistic error and miscalibration worsen even as classification error is reduced. We have demonstrated that recent advances in neural network architecture and training - model capacity, normalization, and regularization

- have strong effects on network calibration. It remains
future work to understand why these trends affect calibration while improving accuracy. Nevertheless, simple techniques can effectively remedy the miscalibration phenomenon in neural networks. Temperature scaling is the simplest, fastest, and most straightforward of the methods, and surprisingly is often the most effective.

**Acknowledgments**

The authors are supported in part by the III-1618134, III1526012, and IIS-1149882 grants from the National Science Foundation, as well as the Bill and Melinda Gates
Foundation and the Office of Naval Research.

**References**

Bengio, Yoshua, Goodfellow, Ian J, and Courville, Aaron.

Deep learning. _Nature_, 521:436–444, 2015.

Bojarski, Mariusz, Del Testa, Davide, Dworakowski,

Daniel, Firner, Bernhard, Flepp, Beat, Goyal, Prasoon,
Jackel, Lawrence D, Monfort, Mathew, Muller, Urs,
Zhang, Jiakai, et al. End to end learning for self-driving cars. _arXiv preprint arXiv:1604.07316_, 2016.

Caruana, Rich, Lou, Yin, Gehrke, Johannes, Koch, Paul,

Sturm, Marc, and Elhadad, Noemie. Intelligible models for healthcare: Predicting pneumonia risk and hospital
30-day readmission. In _KDD_, 2015.

Collobert, Ronan, Kavukcuoglu, Koray, and Farabet,

Cl´ement. Torch7: A matlab-like environment for machine learning. In _BigLearn Workshop, NIPS_, 2011.

Cosmides, Leda and Tooby, John. Are humans good intu itive statisticians after all? rethinking some conclusions from the literature on judgment under uncertainty. _cog-_
_nition_, 58(1):1–73, 1996.

DeGroot, Morris H and Fienberg, Stephen E. The compar ison and evaluation of forecasters. _The_ _statistician_, pp.
12–22, 1983.

Deng, Jia, Dong, Wei, Socher, Richard, Li, Li-Jia, Li, Kai,

and Fei-Fei, Li. Imagenet: A large-scale hierarchical image database. In _CVPR_, pp. 248–255, 2009.

Denker, John S and Lecun, Yann. Transforming neural-net

output levels to probability distributions. In _NIPS_, pp.
853–859, 1990.

Friedman, Jerome, Hastie, Trevor, and Tibshirani, Robert.

_The elements of statistical learning_, volume 1. Springer series in statistics Springer, Berlin, 2001.

Gal, Yarin and Ghahramani, Zoubin. Dropout as a bayesian

approximation: Representing model uncertainty in deep learning. In _ICML_, 2016.

Girshick, Ross. Fast r-cnn. In _ICCV_, pp. 1440–1448, 2015.

Hannun, Awni, Case, Carl, Casper, Jared, Catanzaro,

Bryan, Diamos, Greg, Elsen, Erich, Prenger, Ryan,
Satheesh, Sanjeev, Sengupta, Shubho, Coates, Adam, et al. Deep speech: Scaling up end-to-end speech recognition. _arXiv preprint arXiv:1412.5567_, 2014.

He, Kaiming, Zhang, Xiangyu, Ren, Shaoqing, and Sun,

Jian. Deep residual learning for image recognition. In
_CVPR_, pp. 770–778, 2016.

Hendrycks, Dan and Gimpel, Kevin. A baseline for de tecting misclassified and out-of-distribution examples in neural networks. In _ICLR_, 2017.

Hinton, Geoffrey, Vinyals, Oriol, and Dean, Jeff. Distilling

the knowledge in a neural network. 2015.

Huang, Gao, Sun, Yu, Liu, Zhuang, Sedra, Daniel, and

Weinberger, Kilian. Deep networks with stochastic depth. In _ECCV_, 2016.

Huang, Gao, Liu, Zhuang, Weinberger, Kilian Q, and

van der Maaten, Laurens. Densely connected convolutional networks. In _CVPR_, 2017.

Ioffe, Sergey and Szegedy, Christian. Batch normalization:

Accelerating deep network training by reducing internal covariate shift. 2015.

Iyyer, Mohit, Manjunatha, Varun, Boyd-Graber, Jordan,

and Daum´e III, Hal. Deep unordered composition rivals syntactic methods for text classification. In _ACL_, 2015.

Jaynes, Edwin T. Information theory and statistical me chanics. _Physical review_, 106(4):620, 1957.

Jiang, Xiaoqian, Osl, Melanie, Kim, Jihoon, and Ohno
Machado, Lucila. Calibrating predictive model estimates to support personalized medicine. _Journal of the Amer-_
_ican_ _Medical_ _Informatics_ _Association_, 19(2):263–274,
2012.

Kendall, Alex and Cipolla, Roberto. Modelling uncertainty

in deep learning for camera relocalization. 2016.

Kendall, Alex and Gal, Yarin. What uncertainties do we

need in bayesian deep learning for computer vision?
_arXiv preprint arXiv:1703.04977_, 2017.

Krause, Jonathan, Stark, Michael, Deng, Jia, and Fei-Fei,

Li. 3d object representations for fine-grained categorization. In _IEEE_ _Workshop_ _on_ _3D_ _Representation_ _and_
_Recognition (3dRR)_, Sydney, Australia, 2013.

Krizhevsky, Alex and Hinton, Geoffrey. Learning multiple

layers of features from tiny images, 2009.

Kuleshov, Volodymyr and Ermon, Stefano. Reliable con fidence estimation via online learning. _arXiv_ _preprint_
_arXiv:1607.03594_, 2016.

Kuleshov, Volodymyr and Liang, Percy. Calibrated struc tured prediction. In _NIPS_, pp. 3474–3482, 2015.

Lakshminarayanan, Balaji, Pritzel, Alexander, and Blun dell, Charles. Simple and scalable predictive uncertainty estimation using deep ensembles. _arXiv_ _preprint_
_arXiv:1612.01474_, 2016.

LeCun, Yann, Bottou, L´eon, Bengio, Yoshua, and Haffner,

Patrick. Gradient-based learning applied to document recognition. _Proceedings_ _of_ _the_ _IEEE_, 86(11):2278–
2324, 1998.

**Supplementary Materials:** **On Calibration of Modern Neural Networks**

MacKay, David JC. A practical bayesian framework for

backpropagation networks. _Neural_ _computation_, 4(3):
448–472, 1992.

Naeini, Mahdi Pakdaman, Cooper, Gregory F, and
Hauskrecht, Milos. Obtaining well calibrated probabilities using bayesian binning. In _AAAI_, pp. 2901, 2015.

Netzer, Yuval, Wang, Tao, Coates, Adam, Bissacco,

Alessandro, Wu, Bo, and Ng, Andrew Y. Reading digits in natural images with unsupervised feature learning.
In _Deep_ _Learning_ _and_ _Unsupervised_ _Feature_ _Learning_
_Workshop, NIPS_, 2011.

Niculescu-Mizil, Alexandru and Caruana, Rich. Predicting

good probabilities with supervised learning. In _ICML_, pp. 625–632, 2005.

Pereyra, Gabriel, Tucker, George, Chorowski, Jan, Kaiser,

Łukasz, and Hinton, Geoffrey. Regularizing neural networks by penalizing confident output distributions.
_arXiv preprint arXiv:1701.06548_, 2017.

Platt, John et al. Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. _Advances_ _in_ _large_ _margin_ _classifiers_, 10(3):
61–74, 1999.

Simonyan, Karen and Zisserman, Andrew. Very deep con volutional networks for large-scale image recognition. In
_ICLR_, 2015.

Socher, Richard, Perelygin, Alex, Wu, Jean, Chuang, Ja son, Manning, Christopher D., Ng, Andrew, and Potts,
Christopher. Recursive deep models for semantic compositionality over a sentiment treebank. In _EMNLP_, pp.
1631–1642, 2013.

Srivastava, Nitish, Hinton, Geoffrey, Krizhevsky, Alex,

Sutskever, Ilya, and Salakhutdinov, Ruslan. Dropout: A simple way to prevent neural networks from overfitting.
_Journal_ _of_ _Machine_ _Learning_ _Research_, 15:1929–1958,
2014.

Srivastava, Rupesh Kumar, Greff, Klaus, and Schmid huber, J¨urgen. Highway networks. _arXiv_ _preprint_
_arXiv:1505.00387_, 2015.

Tai, Kai Sheng, Socher, Richard, and Manning, Christo pher D. Improved semantic representations from treestructured long short-term memory networks. 2015.

Vapnik, Vladimir N. _Statistical_ _Learning_ _Theory_ . Wiley
Interscience, 1998.

Welinder, P., Branson, S., Mita, T., Wah, C., Schroff, F.,

Belongie, S., and Perona, P. Caltech-UCSD Birds 200.
Technical Report CNS-TR-2010-001, California Institute of Technology, 2010.

Xiong, Wayne, Droppo, Jasha, Huang, Xuedong, Seide,

Frank, Seltzer, Mike, Stolcke, Andreas, Yu, Dong, and Zweig, Geoffrey. Achieving human parity in conversational speech recognition. _arXiv_ _preprint_
_arXiv:1610.05256_, 2016.

Zadrozny, Bianca and Elkan, Charles. Obtaining calibrated probability estimates from decision trees and naive bayesian classifiers. In _ICML_, pp. 609–616, 2001.

Zadrozny, Bianca and Elkan, Charles. Transforming classi fier scores into accurate multiclass probability estimates.
In _KDD_, pp. 694–699, 2002.

Zagoruyko, Sergey and Komodakis, Nikos. Wide residual

networks. In _BMVC_, 2016.

Zhang, Chiyuan, Bengio, Samy, Hardt, Moritz, Recht, Ben jamin, and Vinyals, Oriol. Understanding deep learning requires rethinking generalization. In _ICLR_, 2017.
