import { Box, Button, IconButton, Typography, useTheme } from "@mui/material";
import { tokens } from "../../theme";
import { mockTransactions } from "../../data/mockData";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import EmailIcon from "@mui/icons-material/Email";
import PointOfSaleIcon from "@mui/icons-material/PointOfSale";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import TrafficIcon from "@mui/icons-material/Traffic";
import Header from "../../components/Header";
import LineChart from "../../components/LineChart";
import GeographyChart from "../../components/GeographyChart";
import BarChart from "../../components/BarChart";
import StatBox from "../../components/StatBox";
import ProgressCircle from "../../components/ProgressCircle";
import React, { useState, useEffect } from 'react';
import axios from 'axios';



function Index() {

}



// import axios from 'axios';
async function apply_decode(id, app) {
  console.log(id);
  console.log(app);

  try {
    const response = await axios.post('http://localhost:5004/api/toggle-block', { id, app });
    console.log(response.data);
    alert( app + ' RULE SET ON INTELLIFIREWALL.');
  } catch (error) {
    console.error('Error blocking IPs:', error);
    // Handle error
  }
}

const Dashboard = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

   const [statsData, setStatsData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5002/firstRowItems');
        const data = response.data[0];
        setStatsData(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 1000);
    return () => clearInterval(intervalId);
  }, []);

  
const getIconForSubtitle = (subtitle, colors) => {
  switch (subtitle) {
    case "Traffice MBPS":
      return <EmailIcon sx={{ color: colors.greenAccent[600], fontSize: "26px" }} />;
    case "UnKnown Traffic":
      return <PointOfSaleIcon sx={{ color: colors.greenAccent[600], fontSize: "26px" }} />;
    case "Connected Devices":
      return <PersonAddIcon sx={{ color: colors.greenAccent[600], fontSize: "26px" }} />;
    case "VPN Traffic":
      return <TrafficIcon sx={{ color: colors.greenAccent[600], fontSize: "26px" }} />;
    default:
      return null;
  }
};

  return (
    
    <Box m="20px">
      <div>
            <h1> </h1>
            <Index /> {/* Call the Index component here */}
        </div>
      {/* HEADER -----------------------------------------------------------------------*/}
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="DASHBOARD" subtitle="Welcome to IntelliFirewall dashboard" />

        <Box>
          <Button
            sx={{
              backgroundColor: colors.blueAccent[700],
              color: colors.grey[100],
              fontSize: "14px",
              fontWeight: "bold",
              padding: "10px 20px",
            }}
          >
            <DownloadOutlinedIcon sx={{ mr: "10px" }} />                         {/*DOWNLOD REPORTS BUTTON */} 
            Download Reports
          </Button>



         

        </Box>
      </Box>
      



      

      {/* GRID & CHARTS -----------------------------------------------------------------------*/}
      <Box
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="140px"
        gap="20px"
      >
        {/* ROW 1 */}

        


        {Object.keys(statsData).map((key, index) => (
          <Box
            key={index}
            gridColumn="span 3"
            backgroundColor={colors.primary[400]}
            display="flex"
            alignItems="center"
            justifyContent="center"
          >
            <StatBox
              title={statsData[key]}
              subtitle={key}
              progress="0.75"
              // increase="14%"
              icon={getIconForSubtitle(key)}
            />
          </Box>
        ))}

        {/* ROW 2 ------------------------------------------------------------------------------------------------------*/}
        <Box
          gridColumn="span 8"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
        >
          <Box
            mt="25px"
            p="0 30px"
            display="flex "
            justifyContent="space-between"
            alignItems="center"
          >



{/* <Box height="250px" m="-20px 0 0 0">
  <LiveSpeedChart />
</Box>

             */}




            <Box>
              <Typography
                variant="h5"
                fontWeight="600"
                color={colors.grey[100]}
              >
                LIVE TRAFFICE GRAPH
              </Typography>

              <Typography
                variant="h3"
                fontWeight="bold"
                color={colors.greenAccent[500]}
              >
                100 MBPS
              </Typography>
            </Box>


            
            <Box>
              <IconButton>
                <DownloadOutlinedIcon
                  sx={{ fontSize: "26px", color: colors.greenAccent[500] }}
                />
              </IconButton>
            </Box>
            
          </Box>
          <Box height="250px" m="-20px 0 0 0">
            <LineChart />
          </Box>
        </Box>

{/* Linechart box end  */}



        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          overflow="auto"
        >
          <Box
            display="flex"
            justifyContent="space-between"
            alignItems="center"
            borderBottom={`4px solid ${colors.primary[500]}`}
            colors={colors.grey[100]}
            p="15px"
          >
            <Typography color={colors.grey[100]} variant="h5" fontWeight="600">
              AVAILABLE POLICIES
            </Typography>
          </Box>
          {mockTransactions.map((transaction, i) => (
            <Box
              key={`${transaction.txId}-${i}`}
              display="flex"
              justifyContent="space-between"
              alignItems="center"
              borderBottom={`4px solid ${colors.primary[500]}`}
              p="15px"
            >
              <Box>
                <Typography
                  color={colors.greenAccent[500]}
                  variant="h5"
                  fontWeight="600"
                >
                  {transaction.txId}
                </Typography>
                <Typography color={colors.grey[100]}>
                  {transaction.user}
                </Typography>
              </Box>


              <Box color={colors.grey[100]}>{transaction.date}</Box>
              <button onClick={() => apply_decode(transaction.txId, transaction.user)}
                backgroundColor={colors.greenAccent[500]}
                p="5px 10px"
                borderRadius="4px"
              >
                {transaction.cost}
              </button>
            </Box>
          ))}
        </Box>

        {/* ROW 3 -----------------------------------------------------------------------------*/}
        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          p="30px"
        >
          <Typography variant="h5" fontWeight="600">
            Campaign
          </Typography>
          <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            mt="25px"
          >
            <ProgressCircle size="125" />
            <Typography
              variant="h5"
              color={colors.greenAccent[500]}
              sx={{ mt: "15px" }}
            >
              10GB in 24 Hours
            </Typography>
            <Typography></Typography>
          </Box>
        </Box>
        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ padding: "30px 30px 0 30px" }}
          >
            Papular Apps Traffic
          </Typography>
          <Box height="250px" mt="-20px">
            <BarChart isDashboard={true} />
          </Box>
        </Box>
        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          padding="30px"
        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ marginBottom: "15px" }}
          >
            Geography Based Traffic
          </Typography>
          <Box height="200px">
            <GeographyChart isDashboard={true} />
          </Box>
        </Box>
      </Box>
           


    </Box>

   
  );
};

export default Dashboard;
