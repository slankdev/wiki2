
jq
====

.. code-block:: text

  {
    "foo": {
      "bar": [
      {
        "key": "1-key",
          "value": "1-value"
      },
      {
        "key": "2-key",
        "value": "2-value",
        "option": "2-opt"
      }
      ],
      "baz": [
      {
        "key": "3-key",
        "value": "3-value",
        "option": "3-opt"
      },
      {
        "key": "4-key",
        "value": "4-value"
      }
      ]
    }
  }

.. code-block:: text

  $ cat example.json | jq '.foo.bar'
  [
    {
      "key": "1-key",
      "value": "1-value"
    },
    {
      "key": "2-key",
      "value": "2-value",
      "option": "2-opt"
    }
  ]

  $ cat example.json | jq '.foo.bar[]'
  {
    "key": "1-key",
    "value": "1-value"
  }
  {
    "key": "2-key",
    "value": "2-value",
    "option": "2-opt"
  }

  $ cat example.json | jq '.foo.bar[1]'
  {
    "key": "2-key",
    "value": "2-value",
    "option": "2-opt"
  }

