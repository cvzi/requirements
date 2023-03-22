# requirements
Find updates for packages in requirements.txt on pypi

## Usage

Run `requirements.py` in a folder that contains a `requirements.txt`

Or run `requirements.py path/to/first/requirements.txt path/to/second/requirements.txt`

![Screenrecord](https://github.com/cvzi/requirements/raw/screenshots/video.png)

Once installed the module can be used directly with `requirements` or `python -m requirements`.

It also offers some functions to query pypi and requirements.txt programmatically:

```python
import requirements

requirements.get_versions("lxml")
[<Version('4.9.2')>, <Version('4.9.1')>, <Version('4.9.0')>, <Version('4.8.0')>, ...]

requirements.parse("lxml == 4.0.0")
('lxml', '==', <Version('4.0.0')>, '4.0.0', 0)

requirements.parse_file("requirements.txt")
[('lxml', '==', <Version('4.9.0')>, '4.9.0', 0), ('defusedxml', '>=', <Version('0.6.0')>, '0.6.0', 1)]

requirements.check_files(["requirements.txt"])
{
    'defusedxml': {
        'clause': '=',
        'current_version': packaging.version.Version('0.6.0'),
        'available_versions': [
            packaging.version.Version('0.4'),
            packaging.version.Version('0.4.1'),
            packaging.version.Version('0.5.0'),
            packaging.version.Version('0.6.0'),
            packaging.version.Version('0.7.0'),
            packaging.version.Version('0.7.1')]},
    'lxml': {
        'clause': '==',
        'current_version': packaging.version.Version('4.9.0'),
        'available_versions': [
            packaging.version.Version('4.7.1'),
            packaging.version.Version('4.8.0'),
            packaging.version.Version('4.9.0'),
            packaging.version.Version('4.9.1'),
            packaging.version.Version('4.9.2'),
            ...
]}}
```