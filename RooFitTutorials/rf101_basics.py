from ROOT import RooRealVar, RooDataSet, RooGaussian, RooPlot, RooFit
from ROOT import TCanvas, TAxis

# S e t u p   m o d e l
# ---------------------

# Declare variables x,mean,sigma with associated name, title, initial value and allowed range
x = RooRealVar("x", "x", -10, 10)

mean = RooRealVar("mean", "mean of gaussian", 1, -10, 10)
sigma = RooRealVar("sigma", "width of gaussian", 1, 0.1, 10)

# Build gaussian p.d.f in terms of x,mean and sigma
gauss = RooGaussian("gauss", "gaussian PDF", x, mean, sigma)

# Construct plot frame in 'x'
xframe = x.frame()

# Plot on X
gauss.plotOn(xframe)

# Change sigma value
sigma.setVal(3)

# Plot on X
gauss.plotOn(xframe, RooFit.LineColor(2))

# Generate data (1000 events in x in a gaussian)
data = gauss.generate(x, 10000)

# Make another frame
xframe2 = x.frame()
data.plotOn(xframe2)
gauss.plotOn(xframe2)

# F i t   m o d e l   t o   d a t a

gauss.fitTo(data)

mean.Print()
sigma.Print()

c = TCanvas("rf101_basics", "rf101_basics", 800, 400)
