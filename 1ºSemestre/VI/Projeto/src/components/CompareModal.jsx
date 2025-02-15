import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  useDisclosure,
  Select,
  SelectItem,
  Chip,
} from "@nextui-org/react";
import { useEffect, useState } from "react";

import SpiderChart from "./SpiderChart";
import HelpPopHover from "./HelpPopOver";

const CompareModal = ({ data, country }) => {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [songs, setSongs] = useState();
  const [selectedSongs, setSelectedSongs] = useState([]);
  const [songObjects, setSongObjects] = useState([]);

  useEffect(() => {
    setSongs(
      data.filter((song) =>
        country != "" ? song.country == country : song.country == ""
      )
    );
  }, [data, country]);

  const handleSelectionChange = (keys) => {

    setSelectedSongs([...keys]);

    const selectedObjects = Array.from(keys).map((key) =>
      songs.find((song) => song.daily_rank === key)
    );

    setSongObjects(selectedObjects);
  };

  const information = {
    "About this Visualization" : "This visualization allows you to compare multiple songs, based on their statistics (Dancebility, Energy, Speechiness, Acousticness, Liveness, Valence)",
    "Key Features": [
      "Selection of mulitple songs to allow comparison between various songs",
      "Representation of this statistics using a spider chart",
      "All the songs choosen will be displayed with a different color",
    ],
    "How to use": "In the select component, choose at least 2 songs and then a spider chart will be displayed with information relative to each song. To deselect a song simply open the select component and click on the song that you want to deselect."
  };

  return (
    <div>
      <Button onPress={onOpen} color="secondary">
        Compare Songs
      </Button>
      <Modal
        isOpen={isOpen}
        isDismissable={false}
        onOpenChange={onOpenChange}
        isKeyboardDismissDisabled={true}
        scrollBehavior="inside"
        hideCloseButton
        className="dark"
        size="5xl"
      >
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-row justify-between items-center gap-1 text-white">
                Compare songs from top 10 of {country != "" ?  country : "the World"}
                <HelpPopHover information={information} placement="left" />
              </ModalHeader>
              <ModalBody className="">
                <Select
                  items={songs}
                  label="Songs to compare"
                  placeholder="Select at least 2 songs..."
                  labelPlacement="outside"
                  className="dark w-full text-white"
                  selectionMode="multiple"
                  selectedKeys={selectedSongs}
                  onSelectionChange={handleSelectionChange}
                  description="You can select more than 2 songs and it will display a spider chart for each song"
                >
                  {(song) => (
                    <SelectItem key={song.daily_rank} textValue={song.name}>
                      <div className="flex gap-2 items-center">
                        <div className="">
                          <Chip
                            color="success"
                            variant="bordered"
                            radius="full"
                          >
                            {song.daily_rank}
                          </Chip>
                        </div>
                        <div className="flex flex-col">
                          <span className="text-small">{song.name}</span>
                          <span className="text-tiny text-default-400">
                            {song.artists}
                          </span>
                        </div>
                      </div>
                    </SelectItem>
                  )}
                </Select>
                <div className="grid grid-cols-3 gap-10">
                  {songObjects.length >= 2 &&
                    <div className="space-y-4 items-center">
                      <h3 className="text-white font-semibold">Songs</h3>
                      <SpiderChart songs={songObjects} />
                    </div>
                  }
                </div>
              </ModalBody>
              <ModalFooter>
                <Button
                  color="danger"
                  variant="bordered"
                  onPress={onClose}
                  onClick={() => {setSelectedSongs([]); setSongObjects([]);}}
                >
                  Close
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </div>
  );
};

export default CompareModal;
