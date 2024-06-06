Overview video: https://www.youtube.com/watch?v=KwRRuiCCdmc. See `README.md` for more general info. Below is Awarity-specific...

### Install and Run

1. Fork and clone the repository.
2. Create and activate the virtual environment as described above.
3. Copy `.env.example` and name `.env`, use this file to set environment variables
4. Install the package in editable mode by running the following command from repository root:

```zsh
pip install -e .
```

The package `needlehaystack` is available for import in your test cases. Develop, make changes and test locally.

```zsh
needlehaystack.run_test
```

See `launch.json` for other launch configurations.

### Visualizations

See `CreateVizFromLLMTesting.ipynb` to create visualizations. Explainer video: https://twitter.com/GregKamradt/status/1729573848893579488

### NOTES TO SELF

We'll want to create an Awareness ModelProvider (see openai.py for an example) that will need to either hit the Awareness cloud API endpoint, or a thin wrapper around the Awareness CLI.
