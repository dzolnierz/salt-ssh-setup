{% set device = data['raw']|regex_search('([vhs]d[a-z]): detected capacity')|first %}
resize-disk:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - args:
      - mods: cloud.resizedisk
      - pillar:
          device: {{ device }}
