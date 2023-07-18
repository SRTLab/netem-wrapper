# Network Emulation

This is a simple wrapper to concatenate network conditions using `tc-netem `
by means of a simple configuration file.

### Usage

```python
python emulate.py --config configs/example.json --output output.json
```

Where:

- `config`: this is the path to the configuration file that must have been properly built in order to avoid errors.
- `output`: this is an optional parameter that when present, creates a `json` file with the information about the timestamp and conditions applied.

### Configuration Files

The configuration files have the following structure:

```
{
  "name": "example",
  "interface": "wlp3s0",
  "events": {
    "1": {
      "duration": 5000,
      "rules": [
        "clear"
      ]
    },
    "2": {
      "duration": 15000,
      "rules": [
        "delay 30ms 10ms distribution normal",
        "loss 0.1% 0.25%"
      ]
    },
    "3": {
      "duration": 10000,
      "rules": [
        "delay 50ms"
      ]
    },
    "4": {
      "duration": 5000,
      "rules": [
        "clear"
      ]
    }
  }
}
```

`name`: name of the experiment.

`interface`: interface where the network conditions will be applied.

`repeat`: number of times the experiment will be repeated. Can be either a number, or `forever` to repeat the experiment until the user stops it.

`events`: list of ordered network conditions.

Each `event` should be tagged by an integer that indicates the order. The
range should be from 1 to N, being N the number of events that will be applied.

Inside the event `duration` indicates in milliseconds the duration of the
network conditions.

`rules` is a list of the conditions that will be applied during the event.
This is where the filters from `tc-netem` should be written. For more info,
take a look at the [tc-netem docs](http://man7.org/linux/man-pages/man8/tc-netem.8.html).

A special rule, that has nothing to do with the `tc-netem` commands has been
created. This rule means that all conditions will be cleared. It is recommended
to always have this rule as the last one to make sure the network conditions are
cleared once the simulation has been finished. It can also be used to add
intervals in the simulation with no conditions applied.

It is important to note that each event **overwrites** its predecessor. If
a condition needs to be kept from an event, it should be included in the next event.

### Explanation of [example.json](configs/example.json)

Here follows an explanation of the example provided in the repo.

The configuration is named `example` and the conditions will be applied to
the interface `wlp3s0`. It has a total of 4 events:

1. The first event lasts 5 seconds and there are no conditions applied.
2. Applies a delay that follows a gaussian distribution of mean 30ms and
   standard deviation (jitter) of 10ms. It also adds a 0.1% packet loss with
   a correlation of 0.25%. This correlation is used to simulate burst errors. This
   event has a duration of 15 seconds.
3. This event is 10 second long and adds a constant 50ms delay.
4. The simulation is finished by 5 seconds of cleared conditions.

### Notes

The code has been tested with python 3.6.9. There is no need of additional python libraries.

When specifying the jitter with a rule such as `delay 30ms 10ms`, an
erroneous behaviour has been noted, so it is better to fix the distribution,
such as `delay 30ms 10ms distribution normal`.
