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

### Visualizations

See `CreateVizFromLLMTesting.ipynb` to create visualizations. Explainer video: https://twitter.com/GregKamradt/status/1729573848893579488

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

### GitHub Project Tracking

See https://github.com/orgs/Aspen-AI/projects/6
