# TVB simulations in nipype

## SETUP
```
git clone https://github.com/amandakeasson/tvb_nipype
cd tvb_nipype
conda env create --name tvbenv --file tvb_environment.yml
source activate tvbenv
```
If you are using a Mac, also run this command:

```
echo "backend: TkAgg" > ~/.matplotlib/matplotlibrc
```

## RUNNING TVB_NIPYPE

Put all structural connectivity data in the `input` folder. Each file is a `.mat` file which contains `sc_weights` and `tract_lengths` for a subject.

From within your tvb_nipype directory modify the template file called `tvb_nipype_spec.json`. The `iterables` field are the parameters for which you would like to test multiple values; the `inputs` field are parameters for which you would like to fix at a single value.

Then, simply run 
```
python run_tvb_nipype.py pse_name nproc 
```
where `pse_name` is the name for your set of simualtions and `nproc` is the number of processes to launch in parallel.

## LICENCE

This is released under the MIT licence, but please make sure that you are following 
the licences of our dependencies, for example [tvb-library](https://github.com/the-virtual-brain/tvb-library)
is released under the [GPL licence](https://github.com/the-virtual-brain/tvb-library/blob/trunk/LICENSE).

