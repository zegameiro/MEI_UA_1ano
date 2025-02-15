/* eslint-disable react/prop-types */
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableColumn,
  TableCell,
} from "@nextui-org/react";
import { useEffect, useState } from "react";
import { MdExplicit } from "react-icons/md";
import { FaArrowDownShortWide, FaArrowUpWideShort } from "react-icons/fa6";

import HelpPopHover from "./HelpPopOver";

const Top10 = ({ data, country, setSong, song }) => {
  const [selectedRow, setSelectedRow] = useState(new Set());

  useEffect(() => {
    if (selectedRow.size > 0) setSong(data.at(Object.values(selectedRow)[0]));
    else if (selectedRow.size == 0) setSong(null);
  }, [data, country, selectedRow, song]);

  const information = {
    "About this Visualization":
      "This table displays the top 10 songs from a country of the world or from the entire world",
    "Key Features": [
      "Select a song to see the ranking on all the countries that have the selected song in the top 10 list",
      "In the Name column an explicit icon might appear if the song is considered explicit",
      "The variation column shows the variation of the rank of a song when comparing to last week if a green icon appears it means that the song rose up in the ranking, else if the icon is red than it came down to lower ranking. If no icon is provided then no changes were observed",
    ],
    "How to use":
      "Select a song from the existing ones and the map will be updated with more information. To undo the action of selecting a song simply click on the song that's currently selected",
  };
  return (
    <div className="flex flex-col space-y-5 justify-center">
      <div className="flex flex-row justify-between items-center">
        <h2 className="font-semibold text-center">
          Top 10 List - {country === "" ? "Global" : country}
        </h2>
        <HelpPopHover information={information} placement="left" />
      </div>
      <Table
        aria-label="Top 10 List"
        selectionMode="single"
        removeWrapper
        className="dark"
        left
        selectedKeys={selectedRow}
        onSelectionChange={setSelectedRow}
      >
        <TableHeader>
          <TableColumn>Rank</TableColumn>
          <TableColumn>Name</TableColumn>
          <TableColumn>Variation</TableColumn>
          <TableColumn>Artists</TableColumn>
        </TableHeader>
        <TableBody>
          {data.map((d, i) => (
            <TableRow key={i}>
              <TableCell className="text-green-600">{d.daily_rank}º</TableCell>
              <TableCell>
                {d.name} {d.is_explicit != "False" && <MdExplicit />}
              </TableCell>
              <TableCell>
                {parseInt(d.weekly_movement) > 0 ? (
                  <FaArrowUpWideShort className="text-green-500" />
                ) : parseInt(d.weekly_movement) < 0 ? (
                  <FaArrowDownShortWide className="text-red-600" />
                ) : (
                  ""
                )}
              </TableCell>
              <TableCell>{d.artists}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default Top10;
