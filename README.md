# TVB simulations in nipype

## SETUP:
```
git clone https://github.com/amandakeasson/tvb_nipype
conda env create --name tvbenv --file tvb_environment.yml
source activate tvbenv
mkdir input
mkdir output
```
If you are using a Mac, run this command:

`echo "backend: TkAgg" > ~/.matplotlib/matplotlibrc`

## RUNNING TVB_NIPYPE

From within your tvb_nipype directory modify the template file called `tvb_nipype_spec.json`. The `iterables` are the parameters for which you would like to test multiple values; the `inputs` are parameters for which you would like to test a single value.

Then, simply run `python run_tvb_nipype.py` and all of your simulations will run. 

## LICENCE: 

This is released under the MIT licence, but please make sure that you are following 
the licences of our dependencies, for example [tvb-library](https://github.com/the-virtual-brain/tvb-library)
is released under the [GPL licence](https://github.com/the-virtual-brain/tvb-library/blob/trunk/LICENSE).

