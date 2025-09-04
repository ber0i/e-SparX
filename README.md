# <img src="https://github.com/user-attachments/assets/8646b2ab-0ef4-46f4-ab5d-f935d11ccf4c" alt="e-SparX logo" height="50" valign="bottom"> e-SparX


Welcome to e-SparX! This is your place to (1) accelerate your ML research and (2) boost the impact of your own work. In ML development, we all work through the following **ML pipeline** steps: find and acquire data; investigate, clean, and process the data, set up a training infrastructure, define models, train, and evaluate. While true innovation often happens in the modeling phase, the remaining workflow is time-consuming. In fact, as intermediate pipeline artifacts (e.g., datasets, code, or hyperparameters) are rarely shared, various researchers invest time in work done by others many times already.

e-SparX changes just that. Here, you can view entire ML pipelines from other researchers, reuse their artifacts, and share your own pipelines. This will increase the impact of your work and help you get feedback from other researchers. And obviously, it will save you a ton of time and work. Go ahead and check out the first available pipelines on the [e-SparX Website](https://e-sparx-public.emt.ed.tum.de/) and the [e-SparX paper](https://doi.org/10.1145/3679240.3734617).

Eager to start sharing your own ML projects? So let's get started and look at how we can register our first pipeline!

> **Note**: If you are an e-SparX developer or want to deploy your own e-SparX version, you'll find all information you need in the [Developers README](Dev_README.md). 

## Getting Started

Clone this repository and create a virtual Python environment (Python version 3.12). Next, navigate inside the folder `python_api` within this repository and run the following in your command prompt

```bash
pip install .
```

Now, you can head over to our [starter notebook](starter_notebook.ipynb) to familiarise yourself with the basic usage of the package and build your first small pipeline!

In the following section, we will explain the essential functionalities you will need to use the package seamlessly in your ML projects. To see e-SparX in action in comprehensive ML projects of different nature, check out the usecases for **Wind Power Forecasting** and **Storage Control**! You might have seen the resulting pipelines on the website earlier. The usecases have their own README inside the `usecases` folder.

## The Essentials at a Glance

It makes sense to go through the [starter notebook](starter_notebook.ipynb) before reading this.

### Artifact Types

e-SparX currently supports six artifact types. We will now state those together with their Python register method. You can also inspect all of them visually on the e-SparX website.

- Dataset: `register_dataset_pandas` for `pd.DataFrames` and `register_dataset_free` for all other datasets
- Code: `register_code`
- Model: `register_model_pytorch` for `torch.nn` Modules and `register_model_free` for all other models
- Hyperparameters: `register_hyperparameters`
- Model Parameters: `register_parameters`
- Model Results: `register_results`

For details on required and optional arguments in each method, check out the methods' individual docstrings.

### Setting Connections

There are two ways to define pipeline connections: Specifying the source artifact in the register method (see starter tutorial), or using `esparx.connect`. In `esparx.connect`, you only need to specify the pipeline you're addressing and the source and target artifact you want to connect.

### Updating and Deleting Artifacts, Deleting Pipelines

- You can update an artifact via calling the correct `esparx.register` method again, passing the updated metadata. You cannot change an artifact type or the name of an artifact. You can only update artifacts you've created yourself.
- You can delete artifacts using `delete_artifact`. You can only delete artifacts that you've created yourself.
- You can delete a pipeline once it is completely empty using `delete_pipeline`. You can only delete pipelines that you've created yourself.

### Reusing a Pipeline Fast

You can download all artifacts from a pipeline to your files directly, using the Python method `init_pipeline` or the CLI command `esparx-pipeline-init`. Check their docstring for more details.

### User Management and "Safety"

The current MVP has a minimalistic user management solution. Installing the `esparx` package will store a config file on your machine holding your user ID. This will enable you to update/delete your own artifacts and prevent other users from updating/deleting your work. However, this solution is far from safe. Anyone who knows about your ID can simply set this ID in his/her config file and has full control over your artifacts. For the MVP, this solution is sufficient, but keep in mind that your artifacts are not bullet proof.

## And Now: Use Cases!

To see how the pipelines where created that you can see online, head over to the `usecases` folder! There are two use cases and each holds an entire ML project. The `usecases` folder has an own short README to explain the settings. All data is real, the models where actually trained and the results are real. This will give you an understanding of how you can use e-SparX in realistic ML projects! Have fun!

## License & Citation

This repository is licensed under [GNU Affero General Public License v3.0 (AGPL-3.0)](https://www.gnu.org/licenses/agpl-3.0.en.html).

If you use code from this repository, please cite

## Citation

If you use **e-SparX**, please cite:

```bibtex
@inproceedings{10.1145/3679240.3734617,
  author    = {Schneider, Annika and Schüttler, Lukas and Ruiz de Vargas, Jan Marco and Eichelbeck, Michael and Goebel, Christoph},
  title     = {e-SparX: A Graph-Based Artifact Exchange Platform to Accelerate Machine Learning Research in the Energy Systems Community},
  year      = {2025},
  isbn      = {9798400711251},
  publisher = {Association for Computing Machinery},
  address   = {New York, NY, USA},
  url       = {https://doi.org/10.1145/3679240.3734617},
  doi       = {10.1145/3679240.3734617},
  booktitle = {Proceedings of the 16th ACM International Conference on Future and Sustainable Energy Systems},
  pages     = {436--445},
  series    = {E-Energy '25}
}
