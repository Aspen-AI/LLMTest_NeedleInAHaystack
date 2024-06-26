Overview video: https://www.youtube.com/watch?v=KwRRuiCCdmc. See `README.md` for more general info. Below is Awarity-specific...

### Install and Run

1. Clone the repository.
2. Create and activate a virtual environment.
3. Copy `.env.example` and name `.env`, use this file to set environment variables
4. Install the package in editable mode by running the following command from repository root:

```zsh
pip install -e .
```

The package `needlehaystack` is now available for import in your test cases. Develop, make changes and test locally.

The executable 'needlehaystack.run_test' is now available to run from the command-line:

```zsh
> needlehaystack.run_test -h
```

See `launch.json` for other launch configurations.

### AwarenessCLI Install

1. You must be a member of the Awarity NPM organization first. Create an NPM account, if necessary, and ping Steve for access.
2. Once you have access, create a classic NPM access token here: https://www.npmjs.com/settings/[YOUR_NPM_USERNAME]/tokens.
3. Modify your `.npmrc` file by adding these lines (replacing `[ACCESS_TOKEN]` with the token you just created):
    ```
    @awarity:registry=https://registry.npmjs.org/
    //registry.npmjs.org/:_authToken=[ACCESS_TOKEN]
    ```
4. Install awareness npm package: `npm install -g @awarity/awareness`
5. Add `.awareness` (already provided at the root of this repository) and `.awareness.keys` files (see `.awareness.keys.example`). They just need to be found above any folder you want to search from. DO NOT check-in your `.awareness.keys` file.
6. Add `.avalanche` (already provided at the root of this repository) and `.avalanche.keys` files (see `.avalanche.keys.example`). They just need to be found above any folder you want to search from. DO NOT check-in your `.avalanche.keys` file.
7. To use type `awareness --help` for a list of supported commands. Some examples:
    - To reason over  a weblink: `awareness query "what does this company do?" --uri https://awarity.ai`
    - To reason over a local folder: `awareness query "what was the first game played of bowl season?" --uri ./bowls-2023`
    - To reason over a web search: `awareness serp "tell me about the team behind awarity.ai"`
8. Other notes:
    - You can try different models using the `--model` switch. The default is `--model gpt-4` but you can use `--model synapse-small` to use the ARC 4090 and `--model synapse-medium` to use Llama 3 70b running on Fireworks.ai.  You can see all of the available models in the `.awareness` file.
    - If you want to reason over a list of links (or files & folders) you can create a file (awarity.links or whatever) containing each link on a separate line (like below), and then pass it in to the query command using the `--list` switch instead of the `--uri` switch:
        ```
        https://awarity.ai
        https://awarity.ai/team/
        https://awarity.ai/info/
        https://awarity.ai/contact/
        ```
    - We need to work out the best way to get this into the UI, but here's how to use context with the awareness CLI tool.  There's two switches you add to your call, which can be used in concert to create ongoing conversations with awareness (they work with both the query and serp commands):
        `--create-context` - this will copy the current query & answer to a file called "context.txt" for use in a follow up query.
        `--context context.txt` - this specifies the context information to add to the query.
    - Usage examples:
        ```
        awareness query "what are the key components of this package?" --uri \source\awarity\awareness\packages\awareness-core --create-context
        awareness query "which one would I use to reason over a users query?" --uri \source\awarity\awareness\packages\awareness-core --create-context --context context.txt
        ```

### Test Configuration
See .vscode/launch.json for examples of how to call the tool.

### Test Run Results
Previous non-Awareness run results have been manually archived to ./awarity_results/. When the tool is run for non-Awareness models, contexts are automatically stored in ./contexts/ and results are automatically stored in ./results/.
The results directory acts as a sort of cache in that if the script finds a prior result there, it'll use that instead of making a call to the model. So after test runs, I'll move results to ./awarity_results/ since their existence in the default location can affect future tests.

For Awareness CLI contexts and tool outputs, these each automatically go to ./awarity_results/[RUN_METADATA]/contexts/ and ./awarity_results/[RUN_METADATA]/outputs/, respectively (where [RUN_METADATA] is awareness_[MODEL]_len[VALUE(S)]_depth[VALUE(S)][SINGLE|MULTI]-[datetime]). Results from ./results/ still need to be manually copied over to ./awarity_results/[RUN_METADATA]/results/ for archiving.

IF YOU'RE NOT SEEING THE EVALUATOR GETTING INVOKED: check the ./results/ directory and make sure it's clear!

NOTE: the awarity_results directory has become too large to check-in to GitHub. They've been stored in our shared Engineering gdrive here: https://drive.google.com/drive/folders/1EXbrK_ZEzIkH3dC7cDo-z01KLxkH4wnk?usp=drive_link

### Visualizations

You can use ./awarity_results/create_histogram.py to create a quick histogram of test scores. Launch ```python create_histogram.py``` and enter the path to the results folder (like ```keep/gpt-4-1106-preview_len112000-127500_depth0-100/results```)

Similarly, you can use ./awarity_results/create_heatmap.py to create a heatmap showing the location of test scores in the space of needle context depth vs. context length. Launch ```python create_heatmap.py``` and enter the path to the results folder (like ```keep/gpt-4-1106-preview_len112000-127500_depth0-100/results```). This code was copied and modified from `CreateVizFromLLMTesting.ipynb`, which the original author used to create visualizations (explainer video: https://twitter.com/GregKamradt/status/1729573848893579488).

### GitHub Project Tracking

See https://github.com/orgs/Aspen-AI/projects/6
