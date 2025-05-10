import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Heading, 
  Text, 
  Badge, 
  Flex, 
  Spinner, 
  Button,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Grid,
  GridItem,
  Divider,
  useToast,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Code,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from '@chakra-ui/react';
import { ArrowBackIcon, RepeatIcon } from '@chakra-ui/icons';
import { formatDistanceToNow, format } from 'date-fns';
import { useRouter } from 'next/router';
import { fetchExperimentDetails, startExperiment, stopExperiment } from '../services/api';

// Helper function to get badge color based on experiment state
const getStateColor = (state) => {
  switch (state) {
    case 'STATE_RUNNING':
      return 'green';
    case 'STATE_COMPLETED':
      return 'blue';
    case 'STATE_FAILED':
      return 'red';
    case 'STATE_STOPPED':
      return 'orange';
    case 'STATE_DEFINED':
      return 'gray';
    default:
      return 'gray';
  }
};

// Helper function to format experiment state for display
const formatState = (state) => {
  if (!state) return 'Unknown';
  return state.replace('STATE_', '').toLowerCase().replace(/_/g, ' ');
};

// Helper function to format experiment type for display
const formatType = (type) => {
  if (!type) return 'Unknown';
  return type.replace('TYPE_', '').replace(/_/g, ' ').toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

const ExperimentDetails = ({ experimentId }) => {
  const [experiment, setExperiment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const router = useRouter();
  const toast = useToast();

  // Load experiment details on component mount
  useEffect(() => {
    if (experimentId) {
      loadExperimentDetails();
    }
  }, [experimentId]);

  const loadExperimentDetails = async () => {
    try {
      setLoading(true);
      const data = await fetchExperimentDetails(experimentId);
      setExperiment(data);
      setError(null);
    } catch (err) {
      setError('Failed to load experiment details');
      console.error('Error loading experiment details:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStartExperiment = async () => {
    try {
      await startExperiment(experimentId);
      toast({
        title: 'Experiment started',
        description: `Experiment ${experimentId} has been started successfully.`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      loadExperimentDetails();
    } catch (err) {
      toast({
        title: 'Failed to start experiment',
        description: err.message || 'An error occurred',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleStopExperiment = async () => {
    try {
      await stopExperiment(experimentId);
      toast({
        title: 'Experiment stopped',
        description: `Experiment ${experimentId} has been stopped successfully.`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      loadExperimentDetails();
    } catch (err) {
      toast({
        title: 'Failed to stop experiment',
        description: err.message || 'An error occurred',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  if (loading) {
    return (
      <Flex justify="center" align="center" height="400px">
        <Spinner size="xl" />
      </Flex>
    );
  }

  if (error) {
    return (
      <Alert status="error" variant="subtle" flexDirection="column" alignItems="center" justifyContent="center" textAlign="center" height="400px">
        <AlertIcon boxSize="40px" mr={0} />
        <AlertTitle mt={4} mb={1} fontSize="lg">Error Loading Experiment</AlertTitle>
        <AlertDescription maxWidth="sm">{error}</AlertDescription>
        <Button mt={4} leftIcon={<ArrowBackIcon />} onClick={() => router.push('/experiments')}>
          Back to Experiments
        </Button>
      </Alert>
    );
  }

  if (!experiment) {
    return (
      <Alert status="warning" variant="subtle" flexDirection="column" alignItems="center" justifyContent="center" textAlign="center" height="400px">
        <AlertIcon boxSize="40px" mr={0} />
        <AlertTitle mt={4} mb={1} fontSize="lg">Experiment Not Found</AlertTitle>
        <AlertDescription maxWidth="sm">The experiment you're looking for doesn't exist or you don't have access to it.</AlertDescription>
        <Button mt={4} leftIcon={<ArrowBackIcon />} onClick={() => router.push('/experiments')}>
          Back to Experiments
        </Button>
      </Alert>
    );
  }

  return (
    <Box>
      <Flex justify="space-between" align="center" mb={4}>
        <Button leftIcon={<ArrowBackIcon />} variant="outline" onClick={() => router.push('/experiments')}>
          Back to Experiments
        </Button>
        <Button leftIcon={<RepeatIcon />} onClick={loadExperimentDetails}>
          Refresh
        </Button>
      </Flex>

      <Box mb={6}>
        <Heading size="lg" mb={2}>{experiment.name}</Heading>
        <Flex align="center" mb={2}>
          <Badge colorScheme={getStateColor(experiment.state)} fontSize="0.8em" mr={2}>
            {formatState(experiment.state)}
          </Badge>
          <Text color="gray.500" fontSize="sm">
            ID: {experimentId}
          </Text>
        </Flex>
        <Text color="gray.600" mb={4}>{experiment.description || 'No description provided'}</Text>

        <Flex mt={4} mb={6} gap={4}>
          {experiment.state === 'STATE_DEFINED' && (
            <Button colorScheme="green" onClick={handleStartExperiment}>
              Start Experiment
            </Button>
          )}
          {experiment.state === 'STATE_RUNNING' && (
            <Button colorScheme="orange" onClick={handleStopExperiment}>
              Stop Experiment
            </Button>
          )}
        </Flex>
      </Box>

      <Grid templateColumns="repeat(3, 1fr)" gap={6} mb={6}>
        <Stat>
          <StatLabel>Type</StatLabel>
          <StatNumber>{formatType(experiment.type)}</StatNumber>
        </Stat>
        <Stat>
          <StatLabel>Start Time</StatLabel>
          <StatNumber>
            {experiment.startTime ? format(new Date(experiment.startTime), 'MMM d, yyyy') : 'Not started'}
          </StatNumber>
          {experiment.startTime && (
            <StatHelpText>
              {formatDistanceToNow(new Date(experiment.startTime), { addSuffix: true })}
            </StatHelpText>
          )}
        </Stat>
        <Stat>
          <StatLabel>Last Updated</StatLabel>
          <StatNumber>
            {experiment.lastUpdateTime ? format(new Date(experiment.lastUpdateTime), 'MMM d, yyyy') : 'N/A'}
          </StatNumber>
          {experiment.lastUpdateTime && (
            <StatHelpText>
              {formatDistanceToNow(new Date(experiment.lastUpdateTime), { addSuffix: true })}
            </StatHelpText>
          )}
        </Stat>
      </Grid>

      <Divider mb={6} />

      <Tabs variant="enclosed">
        <TabList>
          <Tab>Details</Tab>
          <Tab>Parameters</Tab>
          <Tab>Results</Tab>
          <Tab>Logs</Tab>
        </TabList>

        <TabPanels>
          <TabPanel>
            <Box>
              <Heading size="md" mb={4}>Experiment Details</Heading>
              <Text mb={4}>{experiment.description || 'No detailed description available.'}</Text>
              
              {experiment.statusMessage && (
                <Alert status={experiment.state === 'STATE_FAILED' ? 'error' : 'info'} mb={4}>
                  <AlertIcon />
                  {experiment.statusMessage}
                </Alert>
              )}
              
              {experiment.metrics && (
                <Box mt={4}>
                  <Heading size="sm" mb={2}>Metrics</Heading>
                  <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                    {Object.entries(experiment.metrics).map(([key, value]) => (
                      <GridItem key={key}>
                        <Stat>
                          <StatLabel>{key}</StatLabel>
                          <StatNumber>{typeof value === 'number' ? value.toFixed(2) : value}</StatNumber>
                        </Stat>
                      </GridItem>
                    ))}
                  </Grid>
                </Box>
              )}
            </Box>
          </TabPanel>
          
          <TabPanel>
            <Box>
              <Heading size="md" mb={4}>Experiment Parameters</Heading>
              {experiment.parameters ? (
                <Code p={4} borderRadius="md" whiteSpace="pre-wrap">
                  {JSON.stringify(experiment.parameters, null, 2)}
                </Code>
              ) : (
                <Text>No parameters available.</Text>
              )}
            </Box>
          </TabPanel>
          
          <TabPanel>
            <Box>
              <Heading size="md" mb={4}>Experiment Results</Heading>
              {experiment.results ? (
                <Code p={4} borderRadius="md" whiteSpace="pre-wrap">
                  {JSON.stringify(experiment.results, null, 2)}
                </Code>
              ) : (
                <Text>No results available yet.</Text>
              )}
            </Box>
          </TabPanel>
          
          <TabPanel>
            <Box>
              <Heading size="md" mb={4}>Experiment Logs</Heading>
              {experiment.logs && experiment.logs.length > 0 ? (
                <Box maxH="400px" overflowY="auto" p={4} bg="gray.50" borderRadius="md">
                  {experiment.logs.map((log, index) => (
                    <Text key={index} fontSize="sm" mb={1}>
                      <Text as="span" fontWeight="bold">{log.timestamp}: </Text>
                      <Text as="span" color={log.level === 'ERROR' ? 'red.500' : 'inherit'}>
                        {log.message}
                      </Text>
                    </Text>
                  ))}
                </Box>
              ) : (
                <Text>No logs available.</Text>
              )}
            </Box>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
};

export default ExperimentDetails;
