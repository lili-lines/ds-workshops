# Online vs Batch learning, presentation

[[slides]]

A model trained once, or a model that keeps learning? <br>
This workshop compares batch and online learning on greenhouse sensor data, where conditions change over time. <br>
Goal: predict the indoor temperature from the outdoor weather, and see which approach keeps up.

## 1. Data

In a greenhouse, the indoor climate depends on the outdoor weather, and this relationship changes over the year: in winter, heating dominates; in spring, it is the sun and ventilation.

UCI Appliances Energy Prediction[^uci]: a time series from January to May 2016, one measurement every 10 minutes.

- Target: average indoor temperature
- Features: outdoor temperature and humidity, wind, time of day

This change over time is called drift: the data no longer looks like the data the model was trained on.

## 2. Model choice

We use a linear regression[^sklearn-lr][^river-lr]: the predicted indoor temperature is a weighted sum of the inputs.

$$
\hat{y} = w_1 x_1 + w_2 x_2 + \dots + w_p x_p + b
$$

$x_1, \dots, x_p$: the features (outdoor temperature and humidity, wind, time of day) <br>
$w_1, \dots, w_p$: the weights, learned by the model <br>
$b$: a constant <br>
$\hat{y}$: the predicted indoor temperature <br>

Learning means finding the weights that minimize the mean squared error (MSE):

$$
\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} \left( y_i - \hat{y}_i \right)^2
$$

- batch (scikit-learn): the solution is computed directly, in one go
- online (river): the weights are corrected at each measurement with a small step in the direction that reduces the error (gradient descent). The size of this step is the learning rate.

We optimize the MSE, and we evaluate with the MAE (section 4), which is easy to read in °C.

## 3. Learning: batch vs online

### 🧊 Batch

We collect past data, train the model once on this whole batch, then use it as is. This is the "classic" approach taught in data science.

Pros + :

- simple and stable: easy to validate and audit
- robust to outliers (if the training data is cleaned)

Cons - :

- the model gets outdated when conditions change (drift)
- needs training data to start
- to update it, you must retrain everything, which needs all past data and computing power

### 🔁 Batch retrained regularly

In practice, the model is often retrained on a schedule (every night, week or month). It is a good compromise, widely used in industry: the model follows changes, with a delay that depends on how often it is retrained.

Pros + :

- follows changes, with a delay
- each version can be checked before use

Cons - :

- keeps all history, and retraining costs computing power every time
- needs training data to start
- the retraining process must be set up and run

### 🌊 Online, with [`river`](https://riverml.xyz)[^river]

The model processes data one by one, in the order it arrives[^wiki-online]. For each new measurement, it:

1. predicts the value,
2. receives the true value,
3. slightly corrects its parameters in the direction that would have reduced the error.

It does not need to keep past data: each measurement is used, then forgotten. For engineers, the idea is close to an adaptive controller, a recursive filter, or the LMS algorithm in signal processing.

Pros + :

- adapts continuously
- no initial training set: learns from the flow
- closer to how things change in real life, outside the lab
- very light: constant memory, minimal computation per measurement. It fits embedded systems and real-time data streams
- no retraining cycle to organize

Cons - :

- it keeps learning, including errors: a faulty sensor "contaminates" the model, which must then unlearn it. Sensor quality checks are needed upstream
- tricky tuning: a learning rate too high makes the model diverge, too low makes it slow to react
- cold start: at first, the model knows nothing and needs time to adapt
- audit: the model changes at every measurement, so its states must be logged to explain a past decision


## 4. Evaluation

Metric: mean absolute error (MAE), in °C[^sklearn-mae][^river-mae].

$$
\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} \left| y_i - \hat{y}_i \right|
$$

$y_i$: the true measured value <br>
$\hat{y}_i$: the value predicted by the model <br>
$n$: the number of measurements <br>

Meaning: on average, how many °C is the model off?

In practice:

- batch: train on a period t, test on the next period t+1, without shuffling the data
- online: the model predicts before it learns (prequential evaluation)

## 5. Results

| Month | 🧊 Frozen batch | 🔁 Retrained batch | 🌊 Online |
|---|---|---|---|
| January | 0.84 | – | 0.93 |
| February | 1.43 | 1.07 | 0.16 |
| March | 1.72 | 0.83 | 0.14 |
| April | 2.81 | 0.89 | 0.14 |
| May | 5.07 | 1.33 | 0.18 |

Table 1: Mean absolute error (MAE), in °C
{ .caption }

How to read it:

- The frozen batch gets steadily worse. In May, it is off by 5 °C on average, because it has never seen spring.
- The retrained batch limits the damage, but lags behind fast changes (early May, when it suddenly gets warmer).
- Online is slightly worse in January (cold start), then stays very accurate, because it constantly follows the recent state of the greenhouse. With a measurement every 10 minutes, the temperature changes little between two measurements, which helps it a lot.

Pitfalls:

- Faulty sensor
- Learning rate

In any case, monitor the model error in production. It is the most reliable way to detect that the model no longer matches reality.

## 6. Going further

Other public sensor datasets to test the approach:

- UCI Occupancy Detection[^occupancy]: temperature, humidity, light, CO₂
- Intel Berkeley Lab[^intel]: 54 sensors, with drift caused by batteries

## References

[^sklearn-lr]: scikit-learn, LinearRegression: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
[^river-lr]: river, LinearRegression: https://riverml.xyz/latest/api/linear-model/LinearRegression/
[^river]: river documentation: https://riverml.xyz
[^wiki-online]: Online machine learning, Wikipedia: https://en.wikipedia.org/wiki/Online_machine_learning
[^sklearn-mae]: scikit-learn, mean_absolute_error: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html
[^river-mae]: river, metrics.MAE: https://riverml.xyz/latest/api/metrics/MAE/
[^uci]: Candanedo, L. (2017). Appliances Energy Prediction. UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction
[^occupancy]: UCI Occupancy Detection: https://archive.ics.uci.edu/dataset/357/occupancy+detection
[^intel]: Intel Berkeley Research Lab, sensor data: http://db.csail.mit.edu/labdata/labdata.html
