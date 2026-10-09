# Selected result tables

[Guide](README.md) · [Data dictionary](../DATA_DICTIONARY.md). Display values are rounded. This page contains selected aggregate results; definitions and analysis scope are given in the guide.

## Overall behavior response profiles

Source: formal behavior-by-tier response profiles. Scene-equal means of absolute responses; all behaviors and both proxies.

| model | proxy | behavior id | effective scene count | response abs mean | response abs ci95 low | response abs ci95 high |
| --- | --- | --- | --- | --- | --- | --- |
| AutoBot | spatial | acceleration | 11866 | 0.0109 | 0.0093 | 0.0126 |
| AutoBot | temporal | acceleration | 11866 | 0.0055 | 0.0050 | 0.0061 |
| AutoBot | spatial | deceleration | 11517 | 0.0090 | 0.0077 | 0.0105 |
| AutoBot | temporal | deceleration | 11517 | 0.0036 | 0.0033 | 0.0039 |
| AutoBot | spatial | lateral maneuver | 6363 | 0.0076 | 0.0060 | 0.0096 |
| AutoBot | temporal | lateral maneuver | 6363 | 0.0024 | 0.0020 | 0.0028 |
| AutoBot | spatial | turning | 3173 | 0.0098 | 0.0076 | 0.0124 |
| AutoBot | temporal | turning | 3173 | 0.0045 | 0.0038 | 0.0054 |
| AutoBot | spatial | stable motion | 20739 | 0.0121 | 0.0109 | 0.0134 |
| AutoBot | temporal | stable motion | 20739 | 0.0057 | 0.0053 | 0.0061 |
| AutoBot | spatial | stationary | 26811 | 0.0082 | 0.0077 | 0.0088 |
| AutoBot | temporal | stationary | 26811 | 0.0042 | 0.0040 | 0.0045 |
| Wayformer | spatial | acceleration | 12553 | 0.0076 | 0.0069 | 0.0084 |
| Wayformer | temporal | acceleration | 12553 | 0.0053 | 0.0050 | 0.0056 |
| Wayformer | spatial | deceleration | 13969 | 0.0126 | 0.0112 | 0.0141 |
| Wayformer | temporal | deceleration | 13969 | 0.0064 | 0.0060 | 0.0068 |
| Wayformer | spatial | lateral maneuver | 9396 | 0.0050 | 0.0043 | 0.0057 |
| Wayformer | temporal | lateral maneuver | 9396 | 0.0033 | 0.0030 | 0.0036 |
| Wayformer | spatial | turning | 4233 | 0.0045 | 0.0038 | 0.0053 |
| Wayformer | temporal | turning | 4233 | 0.0048 | 0.0044 | 0.0053 |
| Wayformer | spatial | stable motion | 20416 | 0.0088 | 0.0081 | 0.0095 |
| Wayformer | temporal | stable motion | 20416 | 0.0056 | 0.0053 | 0.0058 |
| Wayformer | spatial | stationary | 21461 | 0.0383 | 0.0367 | 0.0399 |
| Wayformer | temporal | stationary | 21461 | 0.0189 | 0.0183 | 0.0195 |
| EMP-M | spatial | acceleration | 12022 | 0.0072 | 0.0067 | 0.0078 |
| EMP-M | temporal | acceleration | 12022 | 0.0039 | 0.0038 | 0.0041 |
| EMP-M | spatial | deceleration | 14222 | 0.0074 | 0.0069 | 0.0080 |
| EMP-M | temporal | deceleration | 14222 | 0.0041 | 0.0039 | 0.0042 |
| EMP-M | spatial | lateral maneuver | 10093 | 0.0050 | 0.0047 | 0.0054 |
| EMP-M | temporal | lateral maneuver | 10093 | 0.0023 | 0.0021 | 0.0024 |
| EMP-M | spatial | turning | 4540 | 0.0046 | 0.0042 | 0.0051 |
| EMP-M | temporal | turning | 4540 | 0.0030 | 0.0028 | 0.0033 |
| EMP-M | spatial | stable motion | 18854 | 0.0082 | 0.0078 | 0.0087 |
| EMP-M | temporal | stable motion | 18854 | 0.0044 | 0.0042 | 0.0045 |
| EMP-M | spatial | stationary | 19984 | 0.0142 | 0.0137 | 0.0148 |
| EMP-M | temporal | stationary | 19984 | 0.0080 | 0.0078 | 0.0083 |

## Stationary behavior across physical tiers

Source: formal behavior-by-tier response profiles. This view shows stationary players across the three physical tiers.

| model | proxy | physical tier | effective scene count | response abs mean | response signed mean | response abs median |
| --- | --- | --- | --- | --- | --- | --- |
| AutoBot | spatial | CR | 8665 | 0.0148 | 0.0024 | 0.0004 |
| AutoBot | temporal | CR | 8665 | 0.0063 | 0.0029 | 0.0002 |
| AutoBot | spatial | SR | 19582 | 0.0128 | 0.0033 | 0.0002 |
| AutoBot | temporal | SR | 19582 | 0.0077 | 0.0049 | 6.665e-05 |
| AutoBot | spatial | BG | 23630 | 0.0036 | 4.068e-06 | 3.826e-05 |
| AutoBot | temporal | BG | 23630 | 0.0014 | 0.0001 | 1.565e-05 |
| Wayformer | spatial | CR | 8127 | 0.0423 | 0.0327 | 0.0026 |
| Wayformer | temporal | CR | 8127 | 0.0169 | 0.0123 | 0.0017 |
| Wayformer | spatial | SR | 14925 | 0.0603 | 0.0514 | 0.0015 |
| Wayformer | temporal | SR | 14925 | 0.0310 | 0.0248 | 0.0013 |
| Wayformer | spatial | BG | 10402 | 0.0027 | 0.0005 | 0.0002 |
| Wayformer | temporal | BG | 10402 | 0.0055 | 0.0008 | 0.0001 |
| EMP-M | spatial | CR | 8003 | 0.0180 | 0.0051 | 0.0038 |
| EMP-M | temporal | CR | 8003 | 0.0069 | 0.0027 | 0.0019 |
| EMP-M | spatial | SR | 13925 | 0.0152 | 0.0063 | 0.0021 |
| EMP-M | temporal | SR | 13925 | 0.0103 | 0.0062 | 0.0022 |
| EMP-M | spatial | BG | 6208 | 0.0069 | 0.0010 | 0.0006 |
| EMP-M | temporal | BG | 6208 | 0.0049 | 0.0006 | 0.0012 |
