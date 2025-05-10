import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Table, 
  Thead, 
  Tbody, 
  Tr, 
  Th, 
  Td, 
  Heading, 
  Button, 
  Badge, 
  Flex, 
  Spinner,
  useToast,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  IconButton
} from '@chakra-ui/react';
import { ChevronDownIcon, SettingsIcon } from '@chakra-ui/icons';
import { formatDistanceToNow } from 'date-fns';
import { useRouter } from 'next/router';
import { fetchExperiments, startExperiment, stopExperiment } from '../services/api';

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

const ExperimentList = () => {
  const [experiments, setExperiments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const router = useRouter();
  const toast = useToast();

  // Load experiments on component mount
  useEffect(() => {
    loadExperiments();
    // Set up polling for updates
    const interval = setInterval(loadExperiments, 10000);
    return () => clearInterval(interval);
  }, []);

  const loadExperiments = async () => {
    try {
      setLoading(true);
      const data = await fetchExperiments();
      setExperiments(data);
      setError(null);
    } catch (err) {
      setError('Failed to load experiments');
      console.error('Error loading experiments:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStartExperiment = async (id) => {
    try {
      await startExperiment(id);
      toast({
        title: 'Experiment started',
        description: `Experiment ${id} has been started successfully.`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      loadExperiments();
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

  const handleStopExperiment = async (id) => {
    try {
      await stopExperiment(id);
      toast({
        title: 'Experiment stopped',
        description: `Experiment ${id} has been stopped successfully.`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      loadExperiments();
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

  const handleViewDetails = (id) => {
    router.push(`/experiments/${id}`);
  };

  return (
    <Box>
      <Flex justify="space-between" align="center" mb={4}>
        <Heading size="lg">Experiments</Heading>
        <Button colorScheme="blue" onClick={() => router.push('/experiments/new')}>
          New Experiment
        </Button>
      </Flex>

      {loading && experiments.length === 0 ? (
        <Flex justify="center" align="center" height="200px">
          <Spinner size="xl" />
        </Flex>
      ) : error ? (
        <Box p={4} bg="red.100" color="red.800" borderRadius="md">
          {error}
        </Box>
      ) : experiments.length === 0 ? (
        <Box p={4} bg="gray.100" borderRadius="md" textAlign="center">
          No experiments found. Create your first experiment to get started.
        </Box>
      ) : (
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>Name</Th>
              <Th>Type</Th>
              <Th>Status</Th>
              <Th>Last Updated</Th>
              <Th>Actions</Th>
            </Tr>
          </Thead>
          <Tbody>
            {experiments.map((experiment) => (
              <Tr key={experiment.id}>
                <Td fontWeight="medium">{experiment.name}</Td>
                <Td>{formatType(experiment.type)}</Td>
                <Td>
                  <Badge colorScheme={getStateColor(experiment.state)}>
                    {formatState(experiment.state)}
                  </Badge>
                </Td>
                <Td>
                  {experiment.lastUpdateTime 
                    ? formatDistanceToNow(new Date(experiment.lastUpdateTime), { addSuffix: true }) 
                    : 'N/A'}
                </Td>
                <Td>
                  <Menu>
                    <MenuButton
                      as={IconButton}
                      aria-label="Options"
                      icon={<SettingsIcon />}
                      variant="outline"
                      size="sm"
                    />
                    <MenuList>
                      <MenuItem onClick={() => handleViewDetails(experiment.id)}>
                        View Details
                      </MenuItem>
                      {experiment.state === 'STATE_DEFINED' && (
                        <MenuItem onClick={() => handleStartExperiment(experiment.id)}>
                          Start Experiment
                        </MenuItem>
                      )}
                      {experiment.state === 'STATE_RUNNING' && (
                        <MenuItem onClick={() => handleStopExperiment(experiment.id)}>
                          Stop Experiment
                        </MenuItem>
                      )}
                    </MenuList>
                  </Menu>
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      )}
    </Box>
  );
};

export default ExperimentList;
