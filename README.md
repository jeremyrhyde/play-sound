# play-sound

This play-sound module can be found on Viam registry [here](https://app.viam.com/module/jeremyrhyde/play-sound). It can be added to any robot as a generic component and will output the desired audio via the audio.

This module has only been tested on a Mac with an M1 chip and a Raspberry Pi 4.

## Deploy to robot

### Using the registry

Go to 'Config' tab, then select components. Once on that page, at the bottom select 'Create Component' and select a generic component. From here you should see a section called 'Registry' from which you can select the play-sound module.


## Usage

As this is a Viam module and a generic component it has an associated DoCommand which can be accessed from the other components/service or directly through the CLI. An example of sending a request via the CLI can be seen below:

```sh
viam robot part run --robot "<robot_name>" --location "<location_name>" --organization "<organization_name>" -part "<part_name>"  -d '{"name": "play-sound", "command": {"message":"Hello World"}}' viam.component.generic.v1.GenericService.DoCommand
```

This example assumes the name of the generic component is `play-sound`.

### Request

Currently, this module supports three types of sound requests: `message`, `file`, and `stop`

 Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `message` | string | Optional | A text based message you want to be said. |
| `file` | string | Optional | A filepath to an audio file (such as mp3) you want to be played |
| `stop` | string | Optional | Will stop the current audio instance. |


An example of a `message` request
```json
{
  "message": "Hello World!"
}
```


## Troubleshooting

Should you encounter issues using this module, you can run the underlying play_sound.py code separately from the rest of a Viam server by either running:


 - ```python3 module/play_sound.py ```
 - ```./exec.sh 0 ```

 This should allow better logging and a similar framework for debugging your connection to your chosen audio output device or potential malformations in your requests and responses. 