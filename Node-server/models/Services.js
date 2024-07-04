const exec = require('child_process');
const appDecodeModel  = require('./Decodes');

// Function to block IPs and URLs
async function blockIPs(id, app) {
    try {
        // Fetch IP and URL associated with the provided id and app from your database
        console.log('Type of appDecodeModel:', typeof appDecodeModel);
        const decodeRecord = await appDecodeModel.findOne({ id: id});

        if (!decodeRecord) {
            throw new Error('No record found for the provided ID and App');
        }

        const { ip, url } = decodeRecord;

        // Block the IP using iptables command
        const iptablesCommand = `sudo iptables -I INPUT -s ${ip} -j DROP`;
        exec(iptablesCommand, (error, stdout, stderr) => {
            if (error) {
                console.error('Error blocking IP:', error);
                throw error;
            }
            console.log('IP blocked successfully');
        });

        // Block the URL using hosts file modification
        const hostsCommand = `echo "127.0.0.1 ${url}" | sudo tee -a /etc/hosts`;
        exec(hostsCommand, (error, stdout, stderr) => {
            if (error) {
                console.error('Error blocking URL:', error);
                throw error;
            }
            console.log('URL blocked successfully');
        });

        // Return a success status
        return true;
    } catch (error) {
        console.error('Error in blockIPs function:', error);
        throw error;
    }
}

module.exports = {
    blockIPs
};
