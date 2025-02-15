import { useEffect } from "react";
import * as d3 from "d3";

const SpiderChart = ({ songs }) => {
  useEffect(() => {
    const chartId = "spider-chart";

    const width = 950;
    const height = 600;
    const radius = Math.min(width, height) / 2 - 50;
    const levels = 5; // Number of concentric circles
    const angleSlice = (Math.PI * 2) / 6;

    d3.select(`#${chartId}`).select("svg").remove();

    const svg = d3
      .select(`#${chartId}`)
      .append("svg")
      .attr("width", width)
      .attr("height", height);

    const chartGroup = svg
      .append("g")
      .attr("transform", `translate(${width / 2}, ${height / 2})`);

    const axes = [
      "Dancebility",
      "Energy",
      "Speechiness",
      "Acousticness",
      "Liveness",
      "Valence",
    ];

    // Draw concentric circles
    for (let i = 0; i < levels; i++) {
      const levelRadius = (radius * (i + 1)) / levels;

      chartGroup
        .append("circle")
        .attr("r", levelRadius)
        .attr("fill", "none")
        .attr("stroke", "#666");

      // Add values along each axis
      const levelValue = ((i + 1) / levels).toFixed(2);
      axes.forEach((axis, j) => {
        const x = levelRadius * Math.cos(angleSlice * j - Math.PI / 2);
        const y = levelRadius * Math.sin(angleSlice * j - Math.PI / 2);

        chartGroup
          .append("text")
          .attr("x", x)
          .attr("y", y)
          .attr("text-anchor", "middle")
          .attr("font-size", "10px")
          .attr("fill", "#666")
          .text(levelValue)
          .attr("fill", "white");
      });
    }

    axes.forEach((axis, i) => {
      const x = radius * Math.cos(angleSlice * i - Math.PI / 2);
      const y = radius * Math.sin(angleSlice * i - Math.PI / 2);

      chartGroup
        .append("line")
        .attr("x1", 0)
        .attr("y1", 0)
        .attr("x2", x)
        .attr("y2", y)
        .attr("stroke", "#aaa")
        .attr("stroke-width", 1);

      const labelOffset = 20;
      chartGroup
        .append("text")
        .attr("x", x * (1 + labelOffset / radius))
        .attr("y", y * (1 + labelOffset / radius))
        .attr("text-anchor", "middle")
        .attr("font-size", "10px")
        .text(axis)
        .attr("fill", "white");
    });

    const colors = d3.schemeCategory10;

    songs.forEach((song, songIndex) => {
      const data = [
        { axis: "Danceability", value: song.danceability },
        { axis: "Energy", value: song.energy },
        { axis: "Speechiness", value: song.speechiness },
        { axis: "Acousticness", value: song.acousticness },
        { axis: "Liveness", value: song.liveness },
        { axis: "Valence", value: song.valence },
      ];

      // Prepare data points for the polygon
      const points = data.map((d, i) => {
        const x = d.value * radius * Math.cos(angleSlice * i - Math.PI / 2);
        const y = d.value * radius * Math.sin(angleSlice * i - Math.PI / 2);
        return [x, y];
      });

      // Add the polygon
      chartGroup
        .append("polygon")
        .attr("points", points.map((p) => p.join(",")).join(" "))
        .attr("fill", colors[songIndex % colors.length])
        .attr("fill-opacity", 0.4)
        .attr("stroke", colors[songIndex % colors.length])
        .attr("stroke-width", 2)
        .on("mouseover", function () {
          d3.select(this).attr("fill-opacity", 0.6);
        })
        .on("mouseout", function () {
          d3.select(this).attr("fill-opacity", 0.4);
        });

      // Add data points for the polygon
      points.forEach(([x, y], i) => {
        chartGroup
          .append("circle")
          .attr("cx", x)
          .attr("cy", y)
          .attr("r", 3)
          .attr("fill", colors[songIndex % colors.length]);
      });
    });

    const legendGroup = svg
      .append("g")
      .attr("transform", `translate(${5}, ${30})`);

    songs.forEach((song, i) => {
      const legendEntry = legendGroup
        .append("g")
        .attr("transform", `translate(0, ${i * 20})`);

      // Legend color box
      legendEntry
        .append("rect")
        .attr("width", 15)
        .attr("height", 15)
        .attr("fill", colors[i % colors.length]);

      // Legend text
      legendEntry
        .append("text")
        .attr("x", 20)
        .attr("y", 12)
        .attr("font-size", "12px")
        .text(song.name)
        .attr("fill", "white");
    });
  }, [songs]);

  return <div id="spider-chart"></div>;
};

export default SpiderChart;
