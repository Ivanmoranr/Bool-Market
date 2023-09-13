## Abstract

Candlestick charts are a visual representation that showcases the highest, lowest, opening, and closing prices within a specific time frame. These charts reveal recurring candlestick patterns as a result of predictable human actions and reactions. These patterns encode valuable information within the candlesticks, that traders employ to make informed decisions about when to enter or exit the market.

To simplify the process of pattern recognition, we propose a dual-model system that automatically identifies candlestick patterns. The first model employs LSTM technology with two outputs to classify the specific pattern, while the second model, also utilizing LSTMs with two outputs, pinpoints the dates on which these patterns occurred. In our experiments, this approach demonstrated the capability to automatically identify eight different candlestick patterns with an average accuracy of 68.7% in real-world data.

## Introduction

LSTMs are predominantly employed in the domain of extensive language processing. However, it is important to note that, fundamentally, a tokenized sentence is essentially a delimited collection of individual elements, with each element corresponding to a lexical unit, namely a word. In essence, a sentence constitutes an ordered succession of these lexical units, while a stock timeseries represents a chronological progression of financial data points encapsulated as candlesticks. In light of this analogy, one may contemplate the conceptual assimilation of each candlestick as akin to a linguistic token within a sentence. This perspective facilitates the utilization of LSTM-based analytical methodologies for the examination of time series data.

## Data extraction

Retrieving the data was the hardest part as there weren't many big databases with chart pattern examples. We used the atmatix.pl website which was the best we could find, this website had information about the ticker, the start and the end for every observation of each pattern over the last years. And with this information we got the stock data in csv format.

As the quantity of the real world examples that we had was not sufficient for us, we developed a synthetic data generator. For every observation the pattern of our chosing was on the middle, creating noise with "ar1 * y1 + ar2* y0 + scipy.stats.norm.rvs(mu,sigma)" on each side of it. The pattern was defined by logic and given some random variability to create a lot of different observations for each pattern and avoid overfitting

## Inbalanced dataset

The main problem arised when counting the number of observations we had for each pattern. For the 4 main patterns we had roughly 1500 observations and for the next 4 we had 300. And when training the model the recall was bad because of this inbalance.

The solution was doing data augmentation, giving randomly from 0 to 2/3 of the width of the pattern to each side so that every crop of the same observation is different, and doing that 10 times for every observations of the unbalanced dataset.

fotos

Also we took advantage of the fact that every pattern had there respective "mirrored" one, meaning that the rising wedge had the falling wedge, the double bottom had the double top and so on. So we flipped every pattern upside down and gave them the number of there mirrored patterns.

fotos

## Approaches considered

#### 1st: Turning timeseries into GAF

This idea was taken from Chen, JH., Tsai, YC. Encoding candlesticks as images for pattern classification using convolutional neural networks. Financ Innov 6, 26 (2020). https://doi.org/10.1186/s40854-020-00187-0

In this research paper they discuss the approach that they take is converting for each time series the open, high, low and close to Gramian-Angular-Fields, so that the model could be analyzed and they report having a 90% accuracy which is much better than the LSTMs one.

We decided not to use this approach because at one point we had up to 30000 timeseries, because of augmenting all the input data, and converting timeseries to GAFs was not as quick as you may think with the limited resources and time that we had to finish the project. Also our max length of a timeseries was 450 candles, but the average length was 115, so the padding covered most of the image in some timeseries probably affecting the model

#### 2nd: Different structures with LSTMs

At first we though of having 8 different models that they would identify wether there was the given pattern of if it had none or other patterns. The problem was that the accuracy was just a little better than the baseline of 50% (because we had the same observations for pattern or no pattern), probably because the models where trained on much less data than the models that took all possible patterns

Our next aproach was using the functional API make a model that would output you the classification task of defining the 8 models and the regression task of finding where the pattern started and ended. The problem was that the loss of the regression was much larger than the classification one, so the model wasn't improving in defining the models, but only in defining the dates where they happened. We tried implementing a feature in the .compile method that is called loss_weight, giving it much more weight to the classification task. But this approach didn't work either becuase it just made the classification a bit better but the regression worse

#### 3rd: Using windows

We though of combining the models with a rolling window of variable length to be able to identify several patterns in one timeseries. This was done with the length of the window being 15, 30, 45, 60 and 75% of the timeseries length.

The pattern type was onehotencoded, so with this we had the confidence level with which the model predicts a target. We hoped that the model would output as the most confident one the pattern that we were sure that graphs had, but with this method the accuracy of the model dropped 25%

## Our final approach

We decided to make 2 models, one for regression and another for classification. And combined them with something we called the popping_model. What this does is first look at the hole timeseries to identify a pattern, once it identifies a pattern it splits the timeseries into 2, one from 0 to the start of the pattern and the other from the end of the pattern to the end of the time series; or in the case it decides that there is no pattern it splits the timeseries in half. And then does the same thing in those two timeseries, and it continious doing so until all of the timeseries lengths are below a threshold (we decided 10%)

#### The classification model

We grouped the 8 patterns into 4 families which was our first target, and then defined a binary classification to decide which one it was. This was done because for every pattern we had another that was really similar, for example rising wedge, and asending triangle. This allowed us to make the model's overall accuracy much better.

The model structure was ------------, and the

fotos

#### The regression model

We made a two target model with an intermediate target being the pattern classification (that we are not going to use), and then a final target being the regression output that comes from concatenating the classification output with the rest of the layers. This was done because every model starts and ends the pattern differently so we though that having the model take into account what model is it putting the dates for it would improve the mae, and it did

The model structure was ------------, and the

fotos

#### The hacking model: Puting both models together

Up until now the models that we discussed only were able to identify one pattern per timeseries.
