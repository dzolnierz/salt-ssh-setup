setup:
  runner.state.orchestrate:
    - mods: orchestrations/setup
    - pillar:
        data: {{ data | json() }}
